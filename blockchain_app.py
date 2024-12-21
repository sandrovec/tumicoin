from flask import Flask, request, jsonify
import hashlib
import json
import time

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

# Crear instancia de Flask
app = Flask(__name__)

# Endpoint para obtener la cadena completa
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{"index": block.index, "hash": block.hash, "transactions": block.transactions} for block in blockchain.chain]
    return jsonify(chain_data), 200

# Endpoint para añadir una nueva transacción
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.json
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Faltan campos en la transacción"}), 400
    blockchain.add_transaction(data['sender'], data['recipient'], data['amount'])
    return jsonify({"message": "Transacción añadida"}), 201

# Endpoint para minar un bloque
@app.route('/mine', methods=['POST'])
def mine_block():
    data = request.json
    miner_address = data.get('miner_address')
    if not miner_address:
        return jsonify({"message": "Se requiere la dirección del minero"}), 400
    blockchain.mine_pending_transactions(miner_address)
    return jsonify({"message": "Bloque minado"}), 200

# Ejecutar servidor
if __name__ == '__main__':
    app.run(port=5000)

import os

if __name__ == "__main__":
    # Render asigna un puerto disponible en la variable de entorno PORT
    port = int(os.environ.get("PORT", 5000))  # Por defecto 5000 si PORT no está configurado
    app.run(host="0.0.0.0", port=port)

