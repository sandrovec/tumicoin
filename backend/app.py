from flask import Flask, jsonify, request
from flask_cors import CORS
import hashlib
import json
from datetime import datetime

timestamp = datetime.now()  # Ahora funcionará correctamente



app = Flask(__name__)
CORS(app)

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=1, previous_hash='0')  # Génesis block

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

@app.route('/chain', methods=['GET'])
def chain():
    try:
        chain_data = blockchain.get_chain()
        return jsonify({"chain": chain_data, "length": len(chain_data)}), 200
    except Exception as e:
        app.logger.error(f"Error en el endpoint /chain: {e}")
        return jsonify({"error": "Error al obtener la cadena"}), 500

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        values = request.get_json()
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return jsonify({"error": "Faltan valores en la transacción"}), 400

        index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])
        return jsonify({"message": f"La transacción se agregará al bloque {index}"}), 201
    except Exception as e:
        app.logger.error(f"Error en el endpoint /add_transaction: {e}")
        return jsonify({"error": "Error al agregar la transacción"}), 500

@app.route('/mine', methods=['POST'])
def mine():
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
                if transaction['recipient'] == address:
                    balance += transaction['amount']
                if transaction['sender'] == address:
                    balance -= transaction['amount']

        return jsonify({"address": address, "balance": balance}), 200
    except Exception as e:
        app.logger.error(f"Error en el endpoint /balance: {e}")
        return jsonify({"error": "Error al obtener el saldo"}), 500

def proof_of_work(last_proof):
    proof = 0
    while not valid_proof(last_proof, proof):
        proof += 1
    return proof

def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:4] == "0000"

def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

