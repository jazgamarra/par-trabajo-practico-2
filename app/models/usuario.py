from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasenha = db.Column(db.String(50))
    administrador = db.Column(db.Boolean)
