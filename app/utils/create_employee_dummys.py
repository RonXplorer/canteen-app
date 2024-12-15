from app import db, app
from app.models import Employee

def add_realistic_employees():
    # Lista de nombres más realistas
    with app.app_context():

        employees_data = [
            {"name": "Juan Pérez", "national_id": "1234567801"},
            {"name": "María López", "national_id": "1234567802"},
            {"name": "Carlos García", "national_id": "1234567803"},
            {"name": "Ana González", "national_id": "1234567804"},
            {"name": "Luis Fernández", "national_id": "1234567805"},
            {"name": "Sofía Rodríguez", "national_id": "1234567806"},
            {"name": "José Martínez", "national_id": "1234567807"},
            {"name": "Laura Ramírez", "national_id": "1234567808"},
            {"name": "Pedro Torres", "national_id": "1234567809"},
            {"name": "Lucía Morales", "national_id": "1234567810"},
        ]
        
        # Agregar empleados a la base de datos
        for emp_data in employees_data:
            employee = Employee(name=emp_data["name"], national_id=emp_data["national_id"])
            db.session.add(employee)
        
        # Confirmar los cambios en la base de datos
        db.session.commit()
        print("10 empleados agregados exitosamente.")