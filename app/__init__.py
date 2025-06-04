from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'login' # Or whatever your login route will be

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models import User # Import User model

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Import and register blueprints here if you use them
    # from app.main import bp as main_bp
    # app.register_blueprint(main_bp)

    # For now, let's import routes directly for simplicity in early stages
    from app import routes # Import routes after models and user_loader

    return app
