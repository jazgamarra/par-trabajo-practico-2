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
    from app.routes.clientes import clientes_bp
    from app.routes.proveedores import proveedores_bp
    app.register_blueprint(proveedores_bp, url_prefix='/proveedores')
    app.register_blueprint(auth_bp)
    app.register_blueprint(productos_bp, url_prefix='/productos')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    app.register_blueprint(auditoria_bp, url_prefix='/auditoria')
    app.register_blueprint(clientes_bp, url_prefix='/clientes')
    
    return app
