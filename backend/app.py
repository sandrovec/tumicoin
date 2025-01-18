from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from blockchain import Blockchain
import os

# Configuración inicial
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Cambia esto por una clave segura
CORS(app)

# Inicialización de extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
blockchain = Blockchain()

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    balance = db.Column(db.Float, default=100.0)  # Balance inicial en Tumicoins
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(120), nullable=False)
    recipient = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Inicializar la base de datos
with app.app_context():
    db.create_all()

# Endpoints

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'El usuario ya existe'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': 'Error al registrar usuario', 'details': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={'email': user.email}, expires_delta=timedelta(hours=1))
        return jsonify({'message': 'Inicio de sesión exitoso', 'token': access_token}), 200
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

@app.route('/balance', methods=['GET'])
@jwt_required()
def get_balance():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user['email']).first()
    return jsonify({'balance': user.balance}), 200

@app.route('/transaction', methods=['POST'])
@jwt_required()
def create_transaction():
    current_user = get_jwt_identity()
    data = request.get_json()
    recipient_email = data.get('recipient')
    amount = data.get('amount')

    if not recipient_email or not amount:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    sender = User.query.filter_by(email=current_user['email']).first()
    recipient = User.query.filter_by(email=recipient_email).first()

    if not recipient:
        return jsonify({'error': 'El destinatario no existe'}), 404

    if sender.balance < amount:
        return jsonify({'error': 'Fondos insuficientes'}), 400

    # Actualizar balances
    sender.balance -= amount
    recipient.balance += amount

    # Crear transacción
    transaction = Transaction(sender=sender.email, recipient=recipient.email, amount=amount)
    db.session.add(transaction)

    # Añadir al blockchain
    blockchain.add_transaction(sender.email, recipient.email, amount)
    blockchain.mine_pending_transactions()

    try:
        db.session.commit()
        return jsonify({'message': 'Transacción realizada con éxito'}), 200
    except Exception as e:
        return jsonify({'error': 'Error al realizar la transacción', 'details': str(e)}), 500

@app.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user = get_jwt_identity()
    transactions = Transaction.query.filter(
        (Transaction.sender == current_user['email']) | (Transaction.recipient == current_user['email'])
    ).all()

    result = [
        {
            'sender': t.sender,
            'recipient': t.recipient,
            'amount': t.amount,
            'timestamp': t.timestamp
        } for t in transactions
    ]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
