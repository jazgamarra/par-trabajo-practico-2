from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models.venta import Venta
from app.models.producto import Producto
from app.models.cliente import Cliente  # NUEVO
from app.models.auditoria import Auditoria
from datetime import datetime
from flask import jsonify

ventas_bp = Blueprint('ventas_bp', __name__)

@ventas_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        ventas = Venta.query.filter(Venta.fecha.between(fecha_inicio, fecha_fin)).all()
    else:
        ventas = Venta.query.all()

    total = sum(v.total for v in ventas)

    return render_template('ventas/listado.html', ventas=ventas, total=total)
# Backend (Flask)
@ventas_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    clientes = Cliente.query.all()
    productos = Producto.query.all()

    # Verifica que los productos y clientes no estén vacíos
    print(f"Clientes: {clientes}")
    print(f"Productos: {productos}")

    if request.method == 'POST':
        data = request.get_json()
        cliente_id = data.get('clienteId')
        productos_en_venta = data.get('productos')

        if not cliente_id or not productos_en_venta:
            return jsonify({"error": "Campos incompletos."}), 400

        # El resto del código de la compra...
        # Agregar la venta a la base de datos

    # Verificar que los datos a pasar al template estén correctos
    precios_venta = {str(p.id): p.precio_venta for p in productos}
    print(f"Precios de productos: {precios_venta}")

    return render_template('ventas/agregar.html', clientes=clientes, productos=productos, precios_venta=precios_venta)
