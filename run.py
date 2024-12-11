from app import app, db
from app.utils.admin_utils import create_admin

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()  # Crea el admin inicial si no existe
    app.run(debug=True)