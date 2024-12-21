from flask import Flask, request, jsonify
import hashlib
import json
import time
import os
import sqlite3
import uuid
from flask_cors import CORS  # Importar CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS en toda la aplicación

# Definición del Bloque
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

# Definición de la Blockchain
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

        # Recompensar al minero
        self.pending_transactions = [{
            "sender": "Sistema",
            "recipient": miner_address,
            "amount": self.mining_reward
        }]

# Crear instancia de Blockchain
blockchain = Blockchain()

# Inicializar base de datos SQLite
def init_db():
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        wallet_address TEXT NOT NULL UNIQUE,
        balance REAL DEFAULT 0
    )
    ''')

    # Crear tabla de transacciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        recipient TEXT,
        amount REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    connection.commit()
    connection.close()

init_db()  # Ejecutar al iniciar el servidor

# Página principal
@app.route("/", methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API de Blockchain"}), 200

# Endpoint para obtener la cadena completa
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{
        "index": block.index,
        "hash": block.hash,
        "transactions": block.transactions
    } for block in blockchain.chain]
    return jsonify(chain_data), 200

# Endpoint para añadir una nueva transacción
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        data = request.json
        required_fields = ['sender', 'recipient', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Faltan campos en la transacción"}), 400

        blockchain.add_transaction(data['sender'], data['recipient'], data['amount'])
        return jsonify({"message": "Transacción añadida"}), 201
    except Exception as e:
        return jsonify({"message": f"Error interno: {e}"}), 500

# Endpoint para minar un bloque
@app.route('/mine', methods=['POST'])
def mine_block():
    try:
        data = request.json
        miner_address = data.get('miner_address')
        if not miner_address:
            return jsonify({"message": "Se requiere la dirección del minero"}), 400

        blockchain.mine_pending_transactions(miner_address)
        return jsonify({"message": "Bloque minado"}), 200
    except Exception as e:
        return jsonify({"message": f"Error interno: {e}"}), 500

# Endpoint para registrar un usuario
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        username = data.get('username')
        if not username:
            return jsonify({"message": "Se requiere un nombre de usuario"}), 400

        wallet_address = str(uuid.uuid4())

        connection = sqlite3.connect('blockchain.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (username, wallet_address, balance) VALUES (?, ?, 0)', 
                       (username, wallet_address))
        connection.commit()
        connection.close()

        return jsonify({
            "message": "Usuario registrado con éxito",
            "username": username,
            "wallet_address": wallet_address
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "El nombre de usuario ya existe"}), 400
    except Exception as e:
        return jsonify({"message": f"Error interno: {e}"}), 500

# Endpoint para listar usuarios
@app.route('/users', methods=['GET'])
def get_users():
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username, wallet_address, balance FROM users')
    users = cursor.fetchall()
    connection.close()

    return jsonify([
        {"username": user[0], "wallet_address": user[1], "balance": user[2]}
        for user in users
    ]), 200

# Endpoint para consultar transacciones
@app.route('/transactions', methods=['GET'])
def get_transactions():
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()
    cursor.execute('SELECT sender, recipient, amount, timestamp FROM transactions')
    transactions = cursor.fetchall()
    connection.close()

    return jsonify([
        {"sender": tx[0], "recipient": tx[1], "amount": tx[2], "timestamp": tx[3]}
        for tx in transactions
    ]), 200

# Endpoint para consultar el balance de un usuario
@app.route('/balance/<wallet_address>', methods=['GET'])
def get_balance(wallet_address):
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()
    cursor.execute('SELECT balance FROM users WHERE wallet_address = ?', (wallet_address,))
    balance = cursor.fetchone()
    connection.close()

    if balance is None:
        return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify({"wallet_address": wallet_address, "balance": balance[0]}), 200

# Ejecutar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto dinámico de Render o 5000 localmente
    app.run(host="0.0.0.0", port=port)


