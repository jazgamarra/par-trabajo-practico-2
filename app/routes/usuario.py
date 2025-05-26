from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.usuario import Usuario
from app import db

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/')
def listado():
    if not session.get('admin'):
        return redirect('/')
    usuarios = Usuario.query.all()
    return render_template('usuarios/listado.html', usuarios=usuarios)

@usuarios_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if not session.get('admin'):
        return redirect('/')

    if request.method == 'POST':
        nuevo = Usuario(
            nombre=request.form['nombre'],
            contrasenha=request.form['contrasenha'],
            administrador=True if request.form.get('administrador') == '1' else False
        )
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('usuarios_bp.listado'))

    return render_template('usuarios/agregar.html')

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('admin'):
        return redirect('/')

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.contrasenha = request.form['contrasenha']
        usuario.administrador = True if request.form.get('administrador') == '1' else False
        db.session.commit()
        return redirect(url_for('usuarios_bp.listado'))

    return render_template('usuarios/editar.html', usuario=usuario)
