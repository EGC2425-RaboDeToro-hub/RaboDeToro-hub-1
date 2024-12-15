import os
from flask_mail import Mail, Message
from app.modules.email.repositories import EmailRepository
from core.services.BaseService import BaseService
from dotenv import load_dotenv  # Importa dotenv


class EmailService(BaseService):
    def __init__(self):
        super().__init__(EmailRepository())
        self.sender = None
        self.mail = None

    def init_app(self, app):
        # Carga las variables de entorno desde el archivo .env
        load_dotenv()
        app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
        app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", "587"))
        app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True") == "True"
        app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL", "False") == "True"
        app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
        app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
        app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

        self.mail = Mail(app)
        self.sender = app.config["MAIL_USERNAME"]

    def sendEmail(self, subject, recipients, body, html_body=None):
        msg = Message(subject, sender=self.sender, recipients=recipients)
        msg.body = body
        if html_body:
            msg.html = html_body

        self.mail.send(msg)
