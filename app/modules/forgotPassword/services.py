from app.modules.forgotPassword.repositories import ForgotpasswordRepository
from core.services.BaseService import BaseService
from app.modules.forgotPassword.models import Token
from app import db
from flask import current_app, url_for, abort
from app.modules.auth.models import User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from datetime import datetime
import pytz
from werkzeug.security import generate_password_hash
from app.modules.email.services import EmailService
import re


class ForgotpasswordService(BaseService):
    def __init__(self):
        super().__init__(ForgotpasswordRepository())

    def getSerializer(self):
        return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
  
    def is_valid_email(self, email):
        # Expresión regular simple para validar el correo electrónico
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
    
    def sendEmail(self, email: str) -> str:
        print("Iniciando función sendEmail...")  # Print de inicio

        # Verificación de email válido
        if not self.is_valid_email(email):
            print("Email no es válido, saliendo de la función.")  # Indica un email no válido
            return None

        email_service = EmailService()
        token = None

        # Búsqueda del usuario en la base de datos
        user = User.query.filter_by(email=email).first()
        if not user:
            print("Usuario no encontrado, no se puede generar el token.")  # Indica que no se encontró usuario
            return None
        print(f"Usuario encontrado: {user}")  # Usuario encontrado

        # Generación del serializador y el token
        try:
            s = self.getSerializer()
            token = s.dumps(email, salt="email-confirm")
            print(f"Token generado: {token}")  # Confirmación de token generado
        except Exception as e:
            print(f"Error al generar el token: {e}")
            return None

        # Creación del enlace de restablecimiento
        try:
            link = url_for("forgotPassword.resetPassword", token=token, _external=True)
            body = f"Follow this link to reset your password: {link}"
            print(f"Enlace de restablecimiento creado: {link}")  # Confirmación del enlace
        except Exception as e:
            print(f"Error al crear el enlace de restablecimiento: {e}")
            return None

        # Configuración y envío del correo electrónico
        try:
            print("Iniciando configuración de correo...")  # Inicio de configuración
            email_service.init_app(current_app)
            print("Configuración de correo completada.")  # Confirmación de configuración

            print("Enviando correo a:", email)  # Antes del envío de correo
            email_service.sendEmail("Forgot Password", [email], body)
            print("Correo enviado correctamente.")  # Confirmación del envío
        except Exception as e:
            print(f"Error durante el envío del email: {e}")
            return None

        print("Función sendEmail completada.")
        return token
    
    def addToken(self, token: str):
        if token is not None:
            reset_token = Token(token=token)
            db.session.add(reset_token)
            db.session.commit()

    def getEmailToken(self, token: str) -> str:
        s = self.getSerializer()
        email = s.loads(token, salt="email-confirm", max_age=3600)
        return email

    def checkToken(self, t: str):
        s = self.getSerializer()
        try:
            s.loads(t, salt="email-confirm", max_age=3600)
        except SignatureExpired:
            abort(404)
        except BadTimeSignature:
            abort(404)

    def resetPassword(self, email: str, password: str):
        hashedPassword = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()
        user.password = hashedPassword
        db.session.commit()

    def checkUsedToken(self, t: str):
        token = Token.query.filter_by(token=t).first()
        token.usedTime = datetime.now(pytz.utc)
        db.session.add(token)
        db.session.commit()

    def usedToken(self, t: str):
        token = Token.query.filter_by(token=t).first()
        return token and token.usedTime
