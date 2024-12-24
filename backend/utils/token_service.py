import jwt
from flask import current_app
from datetime import datetime, timedelta

def generate_token(data, expires_in=3600):
    payload = {
        **data,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
