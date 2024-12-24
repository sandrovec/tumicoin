from flask_mail import Message
from flask import current_app
from app import mail

def send_verification_email(email, token):
    link = f"{current_app.config['FRONTEND_URL']}/verify/{token}"
    msg = Message('Verificación de Cuenta', recipients=[email])
    msg.body = f"Por favor verifica tu cuenta haciendo clic aquí: {link}"
    mail.send(msg)
