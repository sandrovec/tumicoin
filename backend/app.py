from flask import Flask, request, jsonify
from blockchain import Blockchain
from db import init_db, create_user, authenticate_user, get_user_balance
from flask_cors import CORS
import jwt
import os
import datetime

# Configuración de la aplicación
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)  # Permitir solicitudes desde Netlify
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkey')

# Inicializar la base de datos
init_db()

# Crear instancia de Blockchain
blockchain = Blockchain()

# Rutas
@app.route("/", methods=['GET'])
def home():
    return jsonify({"message": "Bienvenido a la API de Tumi Coin"}), 200

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Nombre de usuario y contraseña son requeridos"}), 400
    wallet_address = create_user(username, password)
    return jsonify({"message": "Usuario creado con éxito", "wallet_address": wallet_address}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Nombre de usuario y contraseña son requeridos"}), 400
    token = authenticate_user(username, password)
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Credenciales inválidas"}), 401

@app.route("/balance", methods=["GET"])
def balance():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"message": "No se proporcionó token"}), 401

    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        wallet_address = decoded["wallet_address"]
        balance = get_user_balance(wallet_address)
        return jsonify({"balance": balance}), 200
    except IndexError:
        return jsonify({"message": "Formato de token inválido"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401

@app.route("/chain", methods=["GET"])
def chain():
    chain_data = blockchain.get_chain()
    return jsonify({"chain": chain_data}), 200

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json
    sender = data.get("sender")
    recipient = data.get("recipient")
    amount = data.get("amount")
    if not sender or not recipient or not amount:
        return jsonify({"message": "Datos incompletos"}), 400

    # Lógica para añadir una transacción a la blockchain
    transaction_result = blockchain.add_transaction(sender, recipient, amount)
    if transaction_result:
        return jsonify({"message": "Transacción añadida con éxito"}), 201
    return jsonify({"message": "Error al añadir transacción"}), 400

# Manejo de errores generales
@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"message": "Error interno del servidor"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
