from app import db

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)  # NUEVO
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

    producto = db.relationship('Producto', backref='ventas')
    cliente = db.relationship('Cliente', backref='ventas')  # NUEVO
