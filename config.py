import os

class Config:
    SECRET_KEY = 'clave-super-secreta'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///par2024.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
