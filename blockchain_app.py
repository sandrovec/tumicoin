from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import hashlib
import json
import time
import bcrypt
import uuid
import os

# Configuración del servidor
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///blockchain.db")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "secret_key")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Modelos de la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    wallet_address = db.Column(db.String(64), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(64), nullable=False)
    recipient = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=time.time)

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self, miner_address):
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            transactions=self.pending_transactions
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        self.pending_transactions = [{
            "sender": "Sistema",
            "recipient": miner_address,
            "amount": self.mining_reward
        }]

blockchain = Blockchain()

# Funciones auxiliares
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

# Rutas
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Faltan datos"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "El usuario ya existe"}), 400

    wallet_address = str(uuid.uuid4())
    password_hash = hash_password(password)

    new_user = User(username=username, password_hash=password_hash, wallet_address=wallet_address)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado", "wallet_address": wallet_address}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({"message": "Credenciales incorrectas"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 200

@app.route("/chain", methods=["GET"])
@jwt_required()
def get_chain():
    chain_data = [{
        "index": block.index,
        "hash": block.hash,
        "transactions": block.transactions
    } for block in blockchain.chain]
    return jsonify(chain_data), 200

@app.route("/mine", methods=["POST"])
@jwt_required()
def mine_block():
    data = request.json
    miner_address = data.get("miner_address")

    if not miner_address:
        return jsonify({"message": "Se requiere dirección del minero"}), 400

    blockchain.mine_pending_transactions(miner_address)
    return jsonify({"message": "Bloque minado"}), 200

# Inicializar base de datos
@app.before_first_request
def initialize_database():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


