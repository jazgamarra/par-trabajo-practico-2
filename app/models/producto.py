from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    unidades = db.Column(db.Integer)
    costo = db.Column(db.Float)
    precio = db.Column(db.Float)
    categoria = db.Column(db.String(50))
