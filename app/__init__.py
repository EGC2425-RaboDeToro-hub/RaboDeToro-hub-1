import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_session import Session

from app.modules.email.services import EmailService
from core.configuration.configuration import get_app_version
from core.managers.module_manager import ModuleManager
from core.managers.config_manager import ConfigManager
from core.managers.error_handler_manager import ErrorHandlerManager
from core.managers.logging_manager import LoggingManager

# Load environment variables
load_dotenv()

# Create the instances
db = SQLAlchemy()
migrate = Migrate()
email_service = EmailService()
session = Session()


def clear_logs_and_sessions():
    if os.path.exists("logs"):
        for file in os.listdir("logs"):
            os.remove(os.path.join("logs", file))
    if os.path.exists("flask_session"):
        for file in os.listdir("flask_session"):
            os.remove(os.path.join("flask_session", file))


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load configuration according to environment
    config_manager = ConfigManager(app)
    config_manager.load_config(config_name=config_name)

    # Ensure SESSION_TYPE is set (if not already)
    app.config.setdefault('SESSION_TYPE', 'filesystem')  # Establece el valor por defecto de sesión en 'filesystem'

    # Initialize SQLAlchemy and Migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize session with the app
    session.init_app(app)

    # Deletes all logs and flask_session files
    clear_logs_and_sessions()
    
    # Register modules
    module_manager = ModuleManager(app)
    module_manager.register_modules()

    # Register login manager
    from flask_login import LoginManager

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.auth.models import User

        return User.query.get(int(user_id))

    # Set up logging
    logging_manager = LoggingManager(app)
    logging_manager.setup_logging()

    # Initialize error handler manager
    error_handler_manager = ErrorHandlerManager(app)
    error_handler_manager.register_error_handlers()

    email_service.init_app(app)
    print("MAIL_SERVER:", app.config.get("MAIL_SERVER"))
    print("MAIL_USERNAME:", app.config.get("MAIL_USERNAME"))

    # Injecting environment variables into jinja context
    @app.context_processor
    def inject_vars_into_jinja():

        # Get all the environment variables
        env_vars = {key: os.getenv(key) for key in os.environ}

        # Add the application version manually
        env_vars["APP_VERSION"] = get_app_version()

        # Ensure DOMAIN variable has a default value if not set
        env_vars["DOMAIN"] = os.getenv("DOMAIN", "localhost")

        # Set Boolean variables for the environment
        flask_env = os.getenv("FLASK_ENV")
        env_vars["DEVELOPMENT"] = flask_env == "development"
        env_vars["PRODUCTION"] = flask_env == "production"

        return env_vars

    return app


app = create_app()
