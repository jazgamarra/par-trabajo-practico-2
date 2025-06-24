from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contrasenha = db.Column(db.String(100), nullable=False)
    administrador = db.Column(db.Boolean, default=False)
