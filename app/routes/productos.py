from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.producto import Producto
from app.models.auditoria import Auditoria
from app import db

productos_bp = Blueprint('productos_bp', __name__)

@productos_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')
    productos = Producto.query.all()
    return render_template('productos/listado.html', productos=productos)

@productos_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    if request.method == 'POST':
        nuevo = Producto(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion'],
            unidades=int(request.form['unidades']),
            precio_compra=float(request.form['precio_compra']),
            precio_venta=float(request.form['precio_venta']),
            categoria=request.form['categoria']
        )
        db.session.add(nuevo)
        db.session.commit()

        aud = Auditoria(
            nombreProducto=nuevo.nombre,
            descripcionProducto=nuevo.descripcion,
            unidadesProducto=nuevo.unidades,
            costoProducto=nuevo.precio_compra,
            precioProducto=nuevo.precio_venta,
            categoriaProducto=nuevo.categoria,
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='CREAR'
        )
        db.session.add(aud)
        db.session.commit()

        return redirect(url_for('productos_bp.listado'))

    return render_template('productos/agregar.html')

@productos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.unidades = int(request.form['unidades'])
        producto.precio_compra = int(request.form['precio_compra'])
        producto.precio_venta = int(request.form['precio_venta'])
        producto.categoria = request.form['categoria']
        db.session.commit()

        aud = Auditoria(
            nombreProducto=producto.nombre,
            descripcionProducto=producto.descripcion,
            unidadesProducto=producto.unidades,
            costoProducto=producto.precio_compra,
            precioProducto=producto.precio_venta,
            categoriaProducto=producto.categoria,
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='EDITAR'
        )
        db.session.add(aud)
        db.session.commit()

        return redirect(url_for('productos_bp.listado'))

    return render_template('productos/editar.html', producto=producto)

@productos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if 'usuario_id' not in session:
        return redirect('/')

    producto = Producto.query.get_or_404(id)

    aud = Auditoria(
        nombreProducto=producto.nombre,
        descripcionProducto=producto.descripcion,
        unidadesProducto=producto.unidades,
        costoProducto=producto.precio_compra,
        precioProducto=producto.precio_venta,
        categoriaProducto=producto.categoria,
        idUsuario=session['usuario_id'],
        nombreUsuario=session['usuario_nombre'],
        descripcionAccion='ELIMINAR'
    )
    db.session.add(aud)
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('productos_bp.listado'))
