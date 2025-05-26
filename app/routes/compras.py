from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models.compra import Compra
from app.models.producto import Producto
from app.models.proveedor import Proveedor
from app.models.auditoria import Auditoria
from datetime import datetime

compras_bp = Blueprint('compras_bp', __name__)

@compras_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')
    compras = Compra.query.all()
    return render_template('compras/listado.html', compras=compras)

@compras_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    proveedores = Proveedor.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        nueva_compra = Compra(
            fecha=datetime.now(),
            proveedor_id=request.form['proveedor_id'],
            producto_id=request.form['producto_id'],
            cantidad=int(request.form['cantidad']),
            precio_unitario=float(request.form['precio_unitario']),
            total=float(request.form['cantidad']) * float(request.form['precio_unitario'])
        )
        db.session.add(nueva_compra)

        # Actualizar inventario
        producto = Producto.query.get(nueva_compra.producto_id)
        #producto.stock += nueva_compra.cantidad
        producto.unidades += nueva_compra.cantidad

        # Auditoria
        aud = Auditoria(
            nombreProducto=producto.nombre,
            descripcionProducto=f"Compra de {nueva_compra.cantidad} unidades",
            unidadesProducto=nueva_compra.cantidad,
            costoProducto=nueva_compra.precio_unitario,
            precioProducto=0,
            categoriaProducto="COMPRA",
            idUsuario=session['usuario_id'],
            nombreUsuario=session['usuario_nombre'],
            descripcionAccion='COMPRA'
        )
        db.session.add(aud)

        db.session.commit()

        return redirect(url_for('compras_bp.listado'))

    return render_template('compras/agregar.html', proveedores=proveedores, productos=productos)
