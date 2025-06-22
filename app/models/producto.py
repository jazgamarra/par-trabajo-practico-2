from app import db

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))
    unidades = db.Column(db.Integer)
    precio_compra = db.Column(db.Integer)  
    precio_venta = db.Column(db.Integer)    
    categoria = db.Column(db.String(50))
