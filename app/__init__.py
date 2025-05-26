from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    from config import Config
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # Importar y registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.productos import productos_bp
    from app.routes.usuario import usuarios_bp
    from app.routes.auditoria import auditoria_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(auditoria_bp, url_prefix='/auditoria')

    return app
