from flask import Blueprint, render_template, session, redirect

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')
