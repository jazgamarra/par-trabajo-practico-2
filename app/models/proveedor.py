from app import db

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(100))
    correo = db.Column(db.String(100))
