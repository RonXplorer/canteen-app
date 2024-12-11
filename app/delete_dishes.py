from app import db
from app.models import Dish, Order  # Asegúrate de importar tu modelo

# Borrar todos los registros de la tabla Dish
def delete_all_dishes():
    try:
        db.session.query(Dish).delete()
        db.session.commit()
        print("Todos los platos fueron eliminados con éxito.")
    except Exception as e:
        db.session.rollback()
        print(f"Ocurrió un error: {e}")

# Llama a la función
# delete_all_dishes()
def delete_all_orders():
    try:
        db.session.query(Order).delete()
        db.session.commit()
        print("Todos los Ordenes fueron eliminados con éxito.")
    except Exception as e:
        db.session.rollback()
        print(f"Ocurrió un error: {e}")

# Llama a la función
delete_all_orders()
