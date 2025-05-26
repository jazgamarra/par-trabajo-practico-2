from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.cliente import Cliente
from app.models.auditoria import Auditoria
from app import db

clientes_bp = Blueprint('clientes_bp', __name__)

@clientes_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')
    clientes = Cliente.query.all()
    return render_template('clientes/listado.html', clientes=clientes)

@clientes_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        nuevo = Cliente(
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            telefono=request.form['telefono'],
            direccion=request.form['direccion']
        )
        db.session.add(nuevo)
        db.session.commit()

        aud = Auditoria(
            nombreProducto=nuevo.nombre,
            descripcionProducto=f"cliente {nuevo.correo}",
            unidadesProducto=0,
            costoProducto=0,
            precioProducto=0,
            categoriaProducto="CLIENTE",
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='CREAR'
        )
        db.session.add(aud)
        db.session.commit()

        return redirect(url_for('clientes_bp.listado'))

    return render_template('clientes/agregar.html')

@clientes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.correo = request.form['correo']
        cliente.telefono = request.form['telefono']
        cliente.direccion = request.form['direccion']
        db.session.commit()

        aud = Auditoria(
            nombreProducto=cliente.nombre,
            descripcionProducto=f"cliente {cliente.correo}",
            unidadesProducto=0,
            costoProducto=0,
            precioProducto=0,
            categoriaProducto="CLIENTE",
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='EDITAR'
        )
        db.session.add(aud)
        db.session.commit()

        return redirect(url_for('clientes_bp.listado'))

    return render_template('clientes/editar.html', cliente=cliente)
