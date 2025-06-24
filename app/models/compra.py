from app import db
from datetime import datetime
import random

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    numero_factura = db.Column(db.String(20), nullable=False, unique=True)  # Nuevo campo
    total = db.Column(db.Integer, nullable=False)

    proveedor = db.relationship('Proveedor', backref='compras')

    def generar_numero_factura(self):
        """Genera un número de factura único basado en la fecha y un código aleatorio"""
        fecha = datetime.now().strftime('%Y%m%d%H%M%S')
        numero_aleatorio = random.randint(1000, 9999)
        return f"{fecha}-{numero_aleatorio}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numero_factura = self.generar_numero_factura()
