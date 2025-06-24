from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
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

    # Obtener las fechas del filtro
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    # Filtrar compras si se proporcionan fechas
    compras = Compra.query

    # Si ambas fechas son proporcionadas, filtrar por ellas
    if fecha_inicio and fecha_fin:
        try:
            desde = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            hasta = datetime.strptime(fecha_fin, '%Y-%m-%d')
            hasta = hasta.replace(hour=23, minute=59, second=59) 
            compras = compras.filter(Compra.fecha >= desde, Compra.fecha <= hasta)
        except ValueError:
            pass    

    compras = compras.all()  # Obtener todas las compras después de aplicar el filtro
    total = sum(c.total for c in compras)  # Calcular el total de compras

    return render_template('compras/listado.html', compras=compras, total=total)

@compras_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario_id' not in session:
        return redirect('/')

    proveedores = Proveedor.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        if request.is_json:  # Si los datos vienen en formato JSON
            data = request.get_json()
            proveedor_id = data.get('proveedor_id')
            producto_id = data.get('producto_id')
            cantidad = data.get('cantidad')
            precio_unitario = data.get('precio_unitario')
        else:  # Si vienen como formulario POST tradicional
            proveedor_id = request.form['proveedor_id']
            producto_id = request.form['producto_id']
            cantidad = request.form.get('cantidad')  # Se usa get para evitar KeyError si no existe
            precio_unitario = request.form.get('precio_unitario')

        # Verificar que los campos necesarios no sean None o vacíos
        if not proveedor_id or not producto_id or not cantidad or not precio_unitario:
            return jsonify({"error": "Faltan campos requeridos."}), 400

        try:
            cantidad = int(cantidad)  # Asegurarse de que cantidad sea un número entero
            precio_unitario = int(precio_unitario)  # Asegurarse de que precio_unitario sea un número entero
        except ValueError:
            return jsonify({"error": "Cantidad y precio deben ser números enteros."}), 400

        # Si los valores son válidos, crear la nueva compra
        nueva_compra = Compra(
            fecha=datetime.now(),
            proveedor_id=proveedor_id,
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            total=cantidad * precio_unitario  # Aquí ya podemos multiplicar sin problemas
        )

        db.session.add(nueva_compra)

        # Actualizar inventario y precio de compra del producto
        producto = Producto.query.get(nueva_compra.producto_id)
        producto.unidades += nueva_compra.cantidad
        producto.precio_compra = nueva_compra.precio_unitario

        # Auditoría
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

    precios_compra = {str(p.id): p.precio_compra for p in productos}
    return render_template('compras/agregar.html', proveedores=proveedores, productos=productos, precios_compra=precios_compra)
