from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from app.models.usuario import Usuario
from app import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/')
def login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def do_login():
    print("📂 BD usada:", current_app.config['SQLALCHEMY_DATABASE_URI'])
    todos = Usuario.query.all()
    print("🧑‍🦱 Usuarios en BD:")
    for u in todos:
        print(f" - {u.nombre} / {u.contrasenha}")

    nombre = request.form['nombre']
    contrasenha = request.form['contrasenha']
    user = Usuario.query.filter_by(nombre=nombre, contrasenha=contrasenha).first()
    if user:
        session['usuario_id'] = user.id
        session['usuario_nombre'] = user.nombre
        session['admin'] = user.administrador
        return redirect('/productos')
    return render_template('login.html', error="Usuario o contraseña incorrectos")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')
