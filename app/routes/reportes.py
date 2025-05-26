from flask import Blueprint, render_template, session, redirect
from datetime import datetime
from app.models.producto import Producto
from app.models.compra import Compra
from app.models.venta import Venta
from app import db

reportes_bp = Blueprint('reportes_bp', __name__)

@reportes_bp.route('/inventario')
def reporte_inventario():
    if 'usuario_id' not in session:
        return redirect('/')

    productos = Producto.query.all()
    return render_template('reportes/inventario.html', productos=productos)

@reportes_bp.route('/movimientos')
def reporte_movimientos():
    if 'usuario_id' not in session:
        return redirect('/')

    ahora = datetime.now()
    mes_actual = ahora.month
    anho_actual = ahora.year

    compras = Compra.query.filter(
        db.extract('month', Compra.fecha) == mes_actual,
        db.extract('year', Compra.fecha) == anho_actual
    ).all()

    ventas = Venta.query.filter(
        db.extract('month', Venta.fecha) == mes_actual,
        db.extract('year', Venta.fecha) == anho_actual
    ).all()

    total_compras = sum([c.total for c in compras])
    total_ventas = sum([v.total for v in ventas])

    return render_template(
        'reportes/movimientos.html',
        compras=compras,
        ventas=ventas,
        total_compras=total_compras,
        total_ventas=total_ventas
    )
