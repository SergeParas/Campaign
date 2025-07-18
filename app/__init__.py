from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .utils import create_admin_user

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    from .admin import admin_bp
    from .guest import guest_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(guest_bp, url_prefix='/guest')

    with app.app_context():
        db.create_all()
        create_admin_user()  # utilitaire pour créer un admin initial

    return app