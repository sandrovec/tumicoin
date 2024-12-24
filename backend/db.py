import sqlite3
import bcrypt
import jwt
import uuid

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        wallet_address TEXT UNIQUE
    )
    ''')
    connection.commit()
    connection.close()

def create_user(username, password):
    wallet_address = str(uuid.uuid4())
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (username, password, wallet_address) VALUES (?, ?, ?)', 
                   (username, hashed_password, wallet_address))
    connection.commit()
    connection.close()
    return wallet_address

def authenticate_user(username, password):
    connection = sqlite3.connect('blockchain.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password, wallet_address FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    connection.close()
    if user and bcrypt.checkpw(password.encode(), user[0].encode()):
        payload = {"wallet_address": user[1]}
        token = jwt.encode(payload, "supersecretkey", algorithm="HS256")
        return token
    return None

def get_user_balance(wallet_address):
    # Aquí puedes implementar lógica para obtener balance real desde la blockchain
    return 100  # Ejemplo estático
