from app import create_app, db
from app.models.producto import Producto
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Crear todas las tablas
    db.create_all()

    # Precargar usuarios
    usuarios = [
        Usuario(nombre="admin", contrasenha="admin", administrador=True),
        Usuario(nombre="user1", contrasenha="1234", administrador=False),
        Usuario(nombre="user2", contrasenha="1234", administrador=True),
    ]

    # Precargar productos
    productos = [
        Producto(nombre="Yerba Mate Pajarito", descripcion="Menta 1kg", unidades=5, costo=5000, precio=7000, categoria="Alimentos"),
        Producto(nombre="Azúcar Morena", descripcion="1kg", unidades=5, costo=6500, precio=9000, categoria="Alimentos"),
        Producto(nombre="Leche Entera Trébol", descripcion="1lt", unidades=7, costo=8000, precio=10000, categoria="Alimentos"),
    ]

    db.session.add_all(usuarios + productos)
    db.session.commit()

    print("✅ Base de datos creada y datos precargados")
