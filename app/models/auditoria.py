from app import db

class Auditoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String(50))
    descripcionProducto = db.Column(db.String(50))
    unidadesProducto = db.Column(db.Integer)
    costoProducto = db.Column(db.Float)
    precioProducto = db.Column(db.Float)
    categoriaProducto = db.Column(db.String(50))
    idUsuario = db.Column(db.Integer)
    nombreUsuario = db.Column(db.String(50))
    descripcionAccion = db.Column(db.String(20))
