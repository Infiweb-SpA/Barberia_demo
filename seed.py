import os
from app import create_app, db
from app.models.models import Admin, Barber, Service
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Crea las tablas si no existen
    db.create_all()

    # 1. Admin por defecto (Credenciales iniciales)
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin', 
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        print("Admin creado: admin / admin123")

    # 2. Datos de Bella Donna (Siguiendo tu estructura de Barber/Service)
    # Nota: Puedes renombrar el modelo Barber a 'Especialista' si lo prefieres luego
    barbers = [
        Barber(name="Mateo Valencia", title="Especialista Senior",
               specialty="Tratamientos de foto-depilación y cuidado cutáneo.",
               experience="15 años", image_url="https://via.placeholder.com/300x400?text=Especialista1"),
        Barber(name="Julián Thorne", title="Técnico Estético",
               specialty="Láser diodo y depilación avanzada.",
               experience="8 años", image_url="https://via.placeholder.com/300x400?text=Especialista2")
    ]
    
    for b in barbers:
        if not Barber.query.filter_by(name=b.name).first():
            db.session.add(b)

    # 3. Lista de Servicios de Estética
    services_data = [
        # Categoría: Rostro
        Service(name="Rostro Completo", description="Sesión de foto-depilación facial.", duration=30, price=15000.0, category="Rostro"),
        Service(name="Bozo / Mentón", description="Depilación zonas pequeñas.", duration=15, price=5000.0, category="Rostro"),
        
        # Categoría: Cuerpo
        Service(name="Axilas", description="Sesión rápida y efectiva.", duration=20, price=8000.0, category="Cuerpo"),
        Service(name="Pierna Completa", description="Tratamiento integral de piernas.", duration=60, price=25000.0, category="Cuerpo"),
        
        # Categoría: Packs
        Service(name="Pack Full Body", description="Axilas + Piernas + Rebaje.", duration=120, price=45000.0, category="Packs")
    ]

    for s in services_data:
        if not Service.query.filter_by(name=s.name).first():
            db.session.add(s)

    db.session.commit()
    print("✅ Base de datos de Bella Donna inicializada correctamente.")