from app import create_app, db
from app.models.models import Admin, Barber, Service
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    # Admin por defecto
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin', password_hash=generate_password_hash('admin123'))
        db.session.add(admin)

    # Barberos de ejemplo
    barbers = [
        Barber(name="Mateo Valencia", title="Master Barber",
               specialty="Afeitado tradicional con navaja y cortes clásicos de época.",
               experience="15 años", image_url="https://via.placeholder.com/300x400?text=Barber1"),
        Barber(name="Julián Thorne", title="Senior Artisan",
               specialty="Degradados modernos y diseño de barba contemporánea.",
               experience="8 años", image_url="https://via.placeholder.com/300x400?text=Barber2"),
        Barber(name="David Rossi", title="The Stylist",
               specialty="Texturizados y tratamientos capilares de alta gama.",
               experience="12 años", image_url="https://via.placeholder.com/300x400?text=Barber3")
    ]
    for b in barbers:
        if not Barber.query.filter_by(name=b.name).first():
            db.session.add(b)

    # Servicios de ejemplo
    services = [
        Service(name="Corte Heritage", description="Corte completo, lavado y peinado.", duration=45, price=35.0, category="Cortes"),
        Service(name="Skin Fade", description="Desvanecido quirúrgico con máquina y navaja.", duration=45, price=40.0, category="Cortes"),
        Service(name="Afeitado Steel", description="Navaja clásica, toallas calientes.", duration=60, price=30.0, category="Barba"),
        Service(name="Perfilado & Marcado", description="Definición de contornos y ajuste.", duration=30, price=20.0, category="Barba"),
        Service(name="Barba Ejecutiva", description="Perfilado, hidratación y cuidado.", duration=30, price=25.0, category="Barba"),
        Service(name="Combo Signature", description="Corte + Barba + Ritual facial.", duration=90, price=55.0, category="Combos")
    ]
    for s in services:
        if not Service.query.filter_by(name=s.name).first():
            db.session.add(s)

    db.session.commit()
    print("Base de datos inicializada con datos de ejemplo.")