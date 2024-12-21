from flask import Flask, request, jsonify
from blockchain import Blockchain
from db import init_db, create_user, authenticate_user, get_user_balance
from flask_cors import CORS
import jwt
import os
import datetime

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configuración secreta
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
    wallet_address = create_user(username, password)
    return jsonify({"message": "Usuario creado con éxito", "wallet_address": wallet_address}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    token = authenticate_user(username, password)
    if token:
        return jsonify({"token": token}), 200
    return jsonify({"message": "Credenciales inválidas"}), 401

@app.route("/balance", methods=["GET"])
def balance():
    token = request.headers.get("Authorization").split(" ")[1]
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        wallet_address = decoded["wallet_address"]
        balance = get_user_balance(wallet_address)
        return jsonify({"balance": balance}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



