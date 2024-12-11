from app.models import User  # Ajusta el import según la ubicación de tu modelo
from app import db
import os

def create_admin():
    """Crea un usuario administrador si no existe."""
    if not User.query.filter_by(role='admin').first():
        print("Creando usuario administrador inicial...")
        admin = User(
            name=os.getenv('ADMIN_USERNAME'),
            email=os.getenv('ADMIN_EMAIL'),
            role='admin',
            is_validated=True
        )
        admin.set_password(os.getenv('ADMIN_PASSWORD'))  # Usa una función de hashing
        db.session.add(admin)
        db.session.commit()
        print("usuario Admin creado")
    else:
        print("usuario Admin ya existe")
