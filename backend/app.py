from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime, timedelta

# Configuración inicial
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Cambia esto por una clave segura
CORS(app)

# Inicialización de extensiones
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Endpoint para registro
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verificar si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'El usuario ya existe'}), 409

    # Hashear la contraseña
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': 'Error al registrar usuario', 'details': str(e)}), 500

# Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # Crear token JWT
        access_token = create_access_token(identity={'email': user.email}, expires_delta=timedelta(hours=1))
        return jsonify({'message': 'Inicio de sesión exitoso', 'token': access_token}), 200
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

# Endpoint protegido para obtener información del usuario
@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user = get_jwt_identity()
    return jsonify({'message': 'Usuario autenticado', 'user': current_user}), 200

# Inicializar base de datos
with app.app_context():
    db.create_all()

# Ejecutar servidor
if __name__ == '__main__':
    app.run(debug=True)

