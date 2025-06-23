from flask import Blueprint, render_template, session, redirect, request
from datetime import datetime
from sqlalchemy import func
from app.models.producto import Producto
from app.models.compra import Compra
from app.models.venta import Venta
from app.models.cliente import Cliente
from app.models.proveedor import Proveedor
from app import db

reportes_bp = Blueprint('reportes_bp', __name__)
timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

@reportes_bp.route('/inventario')
def reporte_inventario():
    if 'usuario_id' not in session:
        return redirect('/')

    productos = Producto.query.all()
    return render_template('reportes/inventario.html', productos=productos, timestamp=timestamp)

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
        total_ventas=total_ventas,
        timestamp=timestamp
    )

@reportes_bp.route('/productos-mas-vendidos')
def productos_mas_vendidos():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = db.session.query(
        Producto.nombre,
        func.sum(Venta.cantidad).label('total_vendida')
    ).join(Producto, Producto.id == Venta.producto_id)

    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt))
        except ValueError:
            pass

    productos_vendidos = query.group_by(Producto.nombre) \
                              .order_by(func.sum(Venta.cantidad).desc()) \
                              .all()

    return render_template(
        'reportes/productos_mas_vendidos.html',
        productos=productos_vendidos,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        timestamp=timestamp
    )

@reportes_bp.route('/top-clientes')
def top_clientes():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = db.session.query(
        Cliente.nombre,
        func.sum(Venta.total).label('total_comprado')
    ).join(Cliente, Cliente.id == Venta.cliente_id)

    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Venta.fecha.between(fecha_inicio_dt, fecha_fin_dt))
        except ValueError:
            pass

    clientes = query.group_by(Cliente.nombre) \
                    .order_by(func.sum(Venta.total).desc()) \
                    .limit(15) \
                    .all()

    return render_template(
        'reportes/top_clientes.html',
        clientes=clientes,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        timestamp=timestamp
    )

@reportes_bp.route('/top-proveedores')
def top_proveedores():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = db.session.query(
        Proveedor.nombre,
        func.sum(Compra.total).label('total_comprado')
    ).join(Proveedor, Proveedor.id == Compra.proveedor_id)

    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Compra.fecha.between(fecha_inicio_dt, fecha_fin_dt))
        except ValueError:
            pass

    proveedores = query.group_by(Proveedor.nombre) \
                       .order_by(func.sum(Compra.total).desc()) \
                       .limit(15) \
                       .all()

    return render_template(
        'reportes/top_proveedores.html',
        proveedores=proveedores,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        timestamp=timestamp
    )

# ---------------------------------------------------------------------------------------------------------------------------
from app.routes import productos
import pdfkit
from flask import make_response

def exportar_pdf(template_name, context, nombre_pdf='reporte.pdf'):
    context['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    html = render_template(template_name, **context)
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'no-outline': None,
    }
    pdf = pdfkit.from_string(html, False, options=options)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename={nombre_pdf}'
    return response

# ---------------------------------------------------------------------------------------------------------------------------

#  Exportar Inventario a PDF
@reportes_bp.route('/inventario/pdf')
def reporte_inventario_pdf():
    if 'usuario_id' not in session:
        return redirect('/')
    productos = Producto.query.all()
    return exportar_pdf('reportes_pdf/inventario_pdf.html', {'productos': productos}, 'inventario.pdf')

#  Exportar Movimientos a PDF
@reportes_bp.route('/movimientos/pdf')
def reporte_movimientos_pdf():
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

    return exportar_pdf(
        'reportes_pdf/movimientos_pdf.html',
        {
            'compras': compras,
            'ventas': ventas,
            'total_compras': total_compras,
            'total_ventas': total_ventas
        },
        'movimientos_pdf.pdf'
    )


#  Exportar Productos Más Vendidos a PDF
@reportes_bp.route('/productos-mas-vendidos/pdf')
def productos_mas_vendidos_pdf():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = db.session.query(
        Producto.nombre,
        func.sum(Venta.cantidad).label('total_vendida')
    ).join(Producto, Producto.id == Venta.producto_id)

    if fecha_inicio and fecha_fin:
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            ff = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Venta.fecha.between(fi, ff))
        except ValueError:
            pass

    productos_vendidos = query.group_by(Producto.nombre) \
                              .order_by(func.sum(Venta.cantidad).desc()) \
                              .all()

    return exportar_pdf(
        'reportes_pdf/productos_mas_vendidos_pdf.html',
        {
            'productos': productos_vendidos,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        },
        'productos_mas_vendidos.pdf'
    )


#  Exportar Top Clientes a PDF
@reportes_bp.route('/top-clientes/pdf')
def top_clientes_pdf():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = db.session.query(
        Cliente.nombre,
        func.sum(Venta.total).label('total_comprado')
    ).join(Cliente, Cliente.id == Venta.cliente_id)

    if fecha_inicio and fecha_fin:
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            ff = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Venta.fecha.between(fi, ff))
        except ValueError:
            pass

    clientes = query.group_by(Cliente.nombre) \
                    .order_by(func.sum(Venta.total).desc()) \
                    .limit(15) \
                    .all()

    return exportar_pdf(
        'reportes_pdf/top_clientes_pdf.html',
        {
            'clientes': clientes,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        },
        'top_clientes.pdf'
    )


#  Exportar Top Proveedores a PDF
@reportes_bp.route('/top-proveedores/pdf')
def top_proveedores_pdf():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = db.session.query(
        Proveedor.nombre,
        func.sum(Compra.total).label('total_comprado')
    ).join(Proveedor, Proveedor.id == Compra.proveedor_id)

    if fecha_inicio and fecha_fin:
        try:
            fi = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            ff = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(Compra.fecha.between(fi, ff))
        except ValueError:
            pass

    proveedores = query.group_by(Proveedor.nombre) \
                       .order_by(func.sum(Compra.total).desc()) \
                       .limit(15) \
                       .all()

    return exportar_pdf(
        'reportes_pdf/top_proveedores_pdf.html',
        {
            'proveedores': proveedores,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        },
        'top_proveedores.pdf'
    )
