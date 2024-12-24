from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import hashlib
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Variables de configuración
load_dotenv()  # Cargar variables desde un archivo .env si existe
PORT = int(os.getenv('PORT', 5000))  # Puerto por defecto: 5000
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Modo debug si está configurado como 'True'
DIFFICULTY = int(os.getenv('DIFFICULTY', 4))  # Dificultad por defecto: 4

# Inicialización de la aplicación Flask
app = Flask(__name__)
# Habilitar CORS para permitir solicitudes desde Netlify
CORS(app, resources={r"/*": {"origins": "https://tumicoin.netlify.app"}}, supports_credentials=True)

# Clase Blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=1, previous_hash='0')  # Crear el bloque génesis

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_chain(self):
        return self.chain

    def add_transaction(self, sender, recipient, amount):
        if not isinstance(sender, str) or not isinstance(recipient, str):
            raise ValueError("El remitente y el destinatario deben ser cadenas de texto.")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("El monto debe ser un número positivo.")
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]


blockchain = Blockchain()

# Prueba de trabajo
def proof_of_work(last_proof):
    proof = 0
    while not valid_proof(last_proof, proof):
        proof += 1
    return proof

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:DIFFICULTY] == "0" * DIFFICULTY

def hash_block(block):
    try:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    except Exception as e:
        raise ValueError(f"No se pudo serializar el bloque: {e}")

# Endpoints de la API

@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':  # Manejar solicitudes preflight
        return '', 204

    try:
        values = request.get_json()
        required = ['name', 'email', 'password']
        if not all(k in values for k in required):
            return jsonify({"error": "Faltan valores requeridos"}), 400

        name = values['name']
        email = values['email']
        password = values['password']

        # Generar una dirección única para el usuario (simula una wallet)
        wallet_address = hashlib.sha256(email.encode()).hexdigest()

        # Aquí podrías almacenar los datos en una base de datos si lo necesitas

        return jsonify({
            "message": "Usuario registrado con éxito",
            "user": {
                "name": name,
                "email": email,
                "wallet_address": wallet_address
            }
        }), 201
    except Exception as e:
        app.logger.error(f"Error en el endpoint /register: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':  # Manejar solicitudes preflight
        return '', 204

    try:
        # Obtener los datos enviados desde el frontend
        values = request.get_json()
        required = ['email', 'password']
        if not all(k in values for k in required):
            return jsonify({"error": "Faltan valores requeridos"}), 400

        email = values['email']
        password = values['password']

        # Simula validación de credenciales (puedes conectar esto a una base de datos)
        if email == "test@example.com" and password == "password123":
            # Credenciales correctas
            return jsonify({
                "message": "Inicio de sesión exitoso",
                "token": "abc123"  # Genera un token real en producción
            }), 200
        else:
            # Credenciales incorrectas
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        app.logger.error(f"Error en el endpoint /login: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/chain', methods=['GET'])
def chain():
    try:
        chain_data = blockchain.get_chain()
        return jsonify({"chain": chain_data, "length": len(chain_data)}), 200
    except Exception as e:
        app.logger.error(f"Error en el endpoint /chain: {e}")
        return jsonify({"error": "Error al obtener la cadena"}), 500

@app.route('/add_transaction', methods=['POST', 'OPTIONS'])
def add_transaction():
    if request.method == 'OPTIONS':  # Manejar solicitudes preflight
        return '', 204

    try:
        values = request.get_json()
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return jsonify({"error": "Faltan valores en la transacción"}), 400

        index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])
        return jsonify({"message": f"La transacción se agregará al bloque {index}"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error en el endpoint /add_transaction: {e}")
        return jsonify({"error": "Error al agregar la transacción"}), 500

@app.route('/mine', methods=['POST', 'OPTIONS'])
def mine():
    if request.method == 'OPTIONS':  # Manejar solicitudes preflight
        return '', 204

    try:
        values = request.get_json()
        miner_address = values.get('miner_address')
        if not miner_address:
            return jsonify({"error": "Falta la dirección del minero"}), 400

        last_block = blockchain.last_block
        proof = proof_of_work(last_block['proof'])
        blockchain.add_transaction(sender="0", recipient=miner_address, amount=1)  # Recompensa

        block = blockchain.create_block(proof, hash_block(last_block))
        return jsonify({"message": "Nuevo bloque minado", "block": block}), 201
    except Exception as e:
        app.logger.error(f"Error en el endpoint /mine: {e}")
        return jsonify({"error": "Error al minar el bloque"}), 500

@app.route('/balance/<address>', methods=['GET'])
def get_balance(address):
    try:
        balance = 0
        for block in blockchain.get_chain():
            for transaction in block['transactions']:
                recipient = transaction.get('recipient')
                sender = transaction.get('sender')
                amount = transaction.get('amount', 0)

                if recipient == address:
                    balance += amount
                if sender == address:
                    balance -= amount

        return jsonify({"address": address, "balance": balance}), 200
    except Exception as e:
        app.logger.error(f"Error en el endpoint /balance: {e}")
        return jsonify({"error": "Error al obtener el saldo"}), 500

# Ejecutar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
