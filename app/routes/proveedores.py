from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.proveedor import Proveedor
from app.models.auditoria import Auditoria
from app import db

proveedores_bp = Blueprint('proveedores_bp', __name__)

@proveedores_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')
    proveedores = Proveedor.query.all()
    return render_template('proveedores/listado.html', proveedores=proveedores)

@proveedores_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        nuevo = Proveedor(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            direccion=request.form['direccion'],
            correo=request.form['correo']
        )
        db.session.add(nuevo)
        db.session.commit()

        aud = Auditoria(
            nombreProducto=nuevo.nombre,
            descripcionProducto=f"proveedor {nuevo.correo}",
            unidadesProducto=0,
            costoProducto=0,
            precioProducto=0,
            categoriaProducto="PROVEEDOR",
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='CREAR'
        )
        db.session.add(aud)
        db.session.commit()

        return redirect(url_for('proveedores_bp.listado'))

    return render_template('proveedores/agregar.html')

@proveedores_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        proveedor.nombre = request.form['nombre']
        proveedor.telefono = request.form['telefono']
        proveedor.direccion = request.form['direccion']
        proveedor.correo = request.form['correo']
        db.session.commit()

        aud = Auditoria(
            nombreProducto=proveedor.nombre,
            descripcionProducto=f"proveedor {proveedor.correo}",
            unidadesProducto=0,
            costoProducto=0,
            precioProducto=0,
            categoriaProducto="PROVEEDOR",
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='EDITAR'
        )
        db.session.add(aud)
        db.session.commit()

        return redirect(url_for('proveedores_bp.listado'))

    return render_template('proveedores/editar.html', proveedor=proveedor)
