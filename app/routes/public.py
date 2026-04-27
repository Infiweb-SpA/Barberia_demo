from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.models import Barber, Service, Appointment
from app import db
from datetime import datetime, date, time

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def inicio():
    services = Service.query.all()[:4]  # limite para mostrar
    return render_template('inicio.html', services=services)

@public_bp.route('/servicios')
def servicios():
    services = Service.query.all()
    return render_template('servicios.html', services=services)

@public_bp.route('/equipo')
def equipo():
    barbers = Barber.query.filter_by(is_active=True).all()
    return render_template('equipo.html', barbers=barbers)

@public_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Solo simulación; podríamos guardar en otro modelo
        flash('Mensaje enviado correctamente. Nos pondremos en contacto pronto.', 'success')
        return redirect(url_for('public.contacto'))
    return render_template('contacto.html')

@public_bp.route('/reservas', methods=['GET', 'POST'])
def reservas():
    barbers = Barber.query.filter_by(is_active=True).all()
    services = Service.query.all()

    if request.method == 'POST':
        # Recoger datos del formulario
        service_id = request.form.get('service_id')
        barber_id = request.form.get('barber_id')
        date_str = request.form.get('date')  # formato YYYY-MM-DD
        time_str = request.form.get('time')  # HH:MM
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        notes = request.form.get('notes')

        # Validación básica
        if not all([service_id, barber_id, date_str, time_str, name, phone]):
            flash('Por favor complete todos los campos obligatorios.', 'danger')
            return render_template('reservas.html', barbers=barbers, services=services,
                                   selected_service=service_id, selected_barber=barber_id,
                                   selected_date=date_str, selected_time=time_str)

        appointment = Appointment(
            client_name=name,
            client_email=email,
            client_phone=phone,
            service_id=int(service_id),
            barber_id=int(barber_id),
            date=datetime.strptime(date_str, '%Y-%m-%d').date(),
            time=datetime.strptime(time_str, '%H:%M').time(),
            notes=notes
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Cita confirmada exitosamente. Le esperamos.', 'success')
        return redirect(url_for('public.reservas'))

    # GET: cargar con datos por defecto
    return render_template('reservas.html', barbers=barbers, services=services,
                           selected_service=None, selected_barber=None,
                           selected_date=None, selected_time=None)

@public_bp.route('/api/horarios_disponibles')
def horarios_disponibles():
    date_str = request.args.get('date')
    barber_id = request.args.get('barber_id')
    if not date_str or not barber_id:
        return {'horarios': []}

    query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    # Horario laboral: 10:00 a 20:00, intervalos de 30 minutos
    slots = []
    start_hour = 10
    end_hour = 20
    for hour in range(start_hour, end_hour):
        for minute in [0, 30]:
            t = time(hour, minute)
            # Verificar si ya está ocupado
            ocupado = Appointment.query.filter_by(
                barber_id=barber_id,
                date=query_date,
                time=t
            ).first()
            if not ocupado:
                slots.append(t.strftime('%H:%M'))
    return {'horarios': slots}