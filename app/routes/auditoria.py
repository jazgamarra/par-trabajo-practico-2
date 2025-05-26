from flask import Blueprint, render_template, session, redirect
from app.models.auditoria import Auditoria

auditoria_bp = Blueprint('auditoria_bp', __name__)

@auditoria_bp.route('/')
def listado():
    if 'usuario_id' not in session:
        return redirect('/')
    auditorias = Auditoria.query.order_by(Auditoria.id.desc()).all()
    return render_template('auditoria/listado.html', auditorias=auditorias)
