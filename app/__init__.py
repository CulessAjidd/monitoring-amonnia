from flask import Flask
from flask_login import LoginManager
from .config import Config
from .extensions import db, migrate
from .routes.auth_routes import auth_bp
from .routes.jadwal_routes import jadwal_bp
from .routes.wilayah_routes import wilayah_bp
from .routes.admin_routes import admin_bp
from .routes.masyarakat_routes import masyarakat_bp
from .routes.dashboard_routes import dashboard_bp
from .extensions import db, migrate, mail, csrf, login_manager
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from app.models.user import User
    from app.models.role import Role
    from app.models.provinsi import Provinsi
    from app.models.kabupaten import Kabupaten
    from app.models.kecamatan import Kecamatan
    # from app.models.kelurahan import Kelurahan

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'


    app.register_blueprint(auth_bp)
    app.register_blueprint(jadwal_bp)
    app.register_blueprint(wilayah_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(masyarakat_bp)
    app.register_blueprint(dashboard_bp)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    if not app.debug:
        # Pastikan folder log ada
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # File log dengan rotating (maks 1MB, simpan 10 file)
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=1024 * 1024, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.info("Flask app startup")

    return app
