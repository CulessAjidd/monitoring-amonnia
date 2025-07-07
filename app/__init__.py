from flask import Flask
from .config import Config
from .extensions import db, migrate
from .routes.auth_routes import auth_bp
from .routes.jadwal_routes import jadwal_bp
from .routes.wilayah_routes import wilayah_bp
from .routes.admin_routes import admin_bp
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from app.models.user import User
    from app.models.role import Role

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(jadwal_bp)
    app.register_blueprint(wilayah_bp)
    app.register_blueprint(admin_bp)

    return app
