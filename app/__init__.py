from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # Or whatever your login route will be

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User # Import User model

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .routes import main_bp # Import the Blueprint
    app.register_blueprint(main_bp) # Register the Blueprint

    return app
