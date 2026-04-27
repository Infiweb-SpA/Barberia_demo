from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.models import Admin, Appointment, Barber, Service
from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Admin.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('public.inicio'))   # <-- Antes: 'admin.login'

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    total_citas = Appointment.query.count()
    citas_hoy = Appointment.query.filter_by(date=datetime.now().date()).count()
    barberos_activos = Barber.query.filter_by(is_active=True).count()
    citas_proximas = Appointment.query.filter(
        Appointment.date >= datetime.now().date()
    ).order_by(Appointment.date, Appointment.time).limit(5).all()
    return render_template('admin/dashboard.html',
                           total_citas=total_citas,
                           citas_hoy=citas_hoy,
                           barberos_activos=barberos_activos,
                           citas_proximas=citas_proximas)

@admin_bp.route('/calendario')
@login_required
def calendario():
    # Mes y año actual, o desde parámetros
    today = datetime.now().date()
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)

    # Primer día del mes y último
    first_day = datetime(year, month, 1).date()
    if month == 12:
        last_day = datetime(year+1, 1, 1).date() - timedelta(days=1)
    else:
        last_day = datetime(year, month+1, 1).date() - timedelta(days=1)

    # Citas del mes
    citas_mes = Appointment.query.filter(
        Appointment.date >= first_day,
        Appointment.date <= last_day
    ).order_by(Appointment.date, Appointment.time).all()

    # Construir calendario
    cal = {}
    for i in range(1, last_day.day + 1):
        d = datetime(year, month, i).date()
        cal[d] = []

    for cita in citas_mes:
        cal[cita.date].append(cita)

    # Navegación de meses
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    return render_template('admin/calendario.html',
                           calendar=cal,
                           year=year,
                           month=month,
                           prev_month=prev_month,
                           prev_year=prev_year,
                           next_month=next_month,
                           next_year=next_year)