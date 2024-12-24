from flask import Blueprint, request, jsonify
from models import User
from db import db
from utils.email_service import send_verification_email
from utils.token_service import generate_token, decode_token

auth = Blueprint('auth', __name__)

# Registro de usuario
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'message': 'Todos los campos son obligatorios'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'El correo ya está registrado'}), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # Enviar correo de verificación
    token = generate_token({'email': email})
    send_verification_email(email, token)

    return jsonify({'message': 'Registro exitoso. Verifica tu correo.'}), 201

# Verificación de correo
@auth.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        data = decode_token(token)
        user = User.query.filter_by(email=data['email']).first()

        if user:
            user.verified = True
            db.session.commit()
            return jsonify({'message': 'Correo verificado exitosamente.'}), 200

    except Exception as e:
        print(e)

    return jsonify({'message': 'Token inválido o expirado.'}), 400

# Inicio de sesión
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Credenciales incorrectas'}), 401

    if not user.verified:
        return jsonify({'message': 'Verifica tu correo antes de iniciar sesión'}), 403

    token = generate_token({'email': user.email})
    return jsonify({'message': 'Inicio de sesión exitoso', 'token': token}), 200
