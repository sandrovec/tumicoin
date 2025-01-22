from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from blockchain import Blockchain  # Importar la clase Blockchain
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

CORS(app, resources={r"/*": {"origins": ["https://tumicoins.com", "https://www.tumicoins.com"]}})

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

blockchain = Blockchain()  # Inicializar la blockchain

# Modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Ruta para registrar usuarios
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

        # Crear cuenta en la blockchain
        blockchain.create_account(email)

        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': 'Error al registrar usuario', 'details': str(e)}), 500

# Ruta para iniciar sesión
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

# Ruta para obtener datos del usuario autenticado
@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    email = current_user['email']

    try:
        balance = blockchain.get_balance(email)
        transactions = blockchain.get_user_transactions(email)
        return jsonify({
            'message': 'Usuario autenticado',
            'user': {
                'email': email,
                'balance': balance,
                'transactions': transactions
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Creación de la base de datos
with app.app_context():
    db.create_all()

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
