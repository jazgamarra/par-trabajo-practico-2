from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models.venta import Venta
from app.models.producto import Producto
from app.models.auditoria import Auditoria
from datetime import datetime

ventas_bp = Blueprint('ventas_bp', __name__)

@ventas_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')
    ventas = Venta.query.all()
    return render_template('ventas/listado.html', ventas=ventas)

@ventas_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    productos = Producto.query.all()

    if request.method == 'POST':
        nueva_venta = Venta(
            fecha=datetime.now(),
            producto_id=request.form['producto_id'],
            cantidad=int(request.form['cantidad']),
            precio_unitario=int(request.form['precio_unitario']),
            total=int(request.form['cantidad']) * int(request.form['precio_unitario'])
        )
        db.session.add(nueva_venta)

        # Actualizar inventario
        producto = Producto.query.get(nueva_venta.producto_id)
        producto.unidades -= nueva_venta.cantidad

        # Auditoría
        aud = Auditoria(
            nombreProducto=producto.nombre,
            descripcionProducto=f"Venta de {nueva_venta.cantidad} unidades",
            unidadesProducto=nueva_venta.cantidad,
            costoProducto=0,
            precioProducto=nueva_venta.precio_unitario,
            categoriaProducto="VENTA",
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='VENTA'
        )
        db.session.add(aud)

        db.session.commit()

        return redirect(url_for('ventas_bp.listado'))

    return render_template('ventas/agregar.html', productos=productos)
