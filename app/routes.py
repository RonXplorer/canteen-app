from flask import abort, flash, redirect, render_template, url_for, request, send_file
from app import app, db
from app.models import User, Dish, Order
from app.forms import LoginForm, RegisterForm, DishForm
from flask_login import login_user, logout_user, login_required, current_user
from app.utils.decorators import role_required
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pandas as pd
import tempfile  # Para manejar carpetas temporales de manera portátil
from PIL import Image, ExifTags



def get_week_range():
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())  # Lunes de esta semana
    return start_of_week, today

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_validated:
        return redirect(url_for('unauthorized'))
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'worker':
        return redirect(url_for('available_dishes'))
    elif current_user.role == 'provider':
        return redirect(url_for('my_dishes'))
    else:
        return redirect(url_for('unauthorized'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              email=form.email.data,
                              role=form.role.data)
        user_to_create.set_password(password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Cuenta creada exitosamente! Sesión iniciada como: {user_to_create.name}', category='success')
        return redirect(url_for('index'))
    if form.errors != {}: # Si hay errores en el formulario
        for err_msg in form.errors.values():
            flash(f'Ooops! ocurrió un error: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user: User = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password(password=form.password.data):
            login_user(attempted_user)
            flash(f'Iniciaste sesión como: {attempted_user.name}', category='success')
            return redirect(url_for('index'))
        else:
            flash('El usuario y contraseña no coinciden! Por favor intenta de nuevo', category='danger')
            return redirect(url_for('login'))
                
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente!', category='info')
    return redirect(url_for('index'))

@app.route('/admin_dashboard')
@role_required('admin')
def admin_dashboard():
    return render_template("admin_dashboard.html", users=User.query.all())

@app.route('/available_dishes')
@role_required('worker')
def available_dishes():
    available_dishes = Dish.query.all()
    return render_template("available_dishes.html", available_dishes=available_dishes)

@app.route('/create_dish', methods=['GET', 'POST'])
@role_required('provider')
def create_dish():
    form = DishForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data

        # Obtener el archivo de imagen
        image_file = form.image_file.data

        if image_file:
            # Asegúrate de que el archivo tiene un nombre seguro
            filename = secure_filename(image_file.filename)
            # Construir la ruta para guardar el archivo
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Guardar el archivo en la ruta indicada
            image_file.save(image_path)

            # Comprimir y corregir orientación de la imagen usando Pillow
            try:
                # Abrir la imagen
                img = Image.open(image_path)

                # Corregir orientación basada en datos EXIF (si existen)
                if hasattr(img, "_getexif"):  # Verifica si hay metadatos EXIF
                    exif = img._getexif()
                    if exif is not None:
                        for tag, value in exif.items():
                            if ExifTags.TAGS.get(tag) == "Orientation":
                                if value == 3:  # Girar 180°
                                    img = img.rotate(180, expand=True)
                                elif value == 6:  # Girar 270° (90° sentido horario)
                                    img = img.rotate(270, expand=True)
                                elif value == 8:  # Girar 90° (90° sentido antihorario)
                                    img = img.rotate(90, expand=True)

                # Redimensionar la imagen si es demasiado grande
                max_size = (800, 800)
                img.thumbnail(max_size)

                # Guardar la imagen con calidad ajustada
                img.save(image_path, quality=85, optimize=True)

            except Exception as e:
                flash(f'Error al procesar la imagen: {e}', category='danger')
                return redirect(url_for('create_dish'))

        else:
            filename = None

        available_start_date = form.available_start_date.data
        available_end_date = form.available_end_date.data

        # Crear un nuevo plato y guardar en la base de datos
        new_dish = Dish(
            name=name,
            description=description, 
            price=price, 
            img_url=filename, 
            provider_id=current_user.id,
            available_start_date=available_start_date,
            available_end_date=available_end_date)

        db.session.add(new_dish)
        db.session.commit()

        flash('¡Plato creado con éxito!', category='success')
        return redirect(url_for('index'))

    if form.errors != {}:  # Si hay errores en el formulario
        for err_msg in form.errors.values():
            flash(f'Ooops! ocurrió un error: {err_msg}', category='danger')

    return render_template('create_dish.html', form=form)


# Ruta para listar platos
@app.route('/my_dishes')
@role_required('provider')
def my_dishes():
    dishes = Dish.query.filter_by(provider_id=current_user.id)
    return render_template('my_dishes.html', dishes=dishes)

@app.route('/delete_dish/<int:dish_id>', methods=['POST'])
@role_required('provider')
def delete_dish(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    db.session.delete(dish)
    db.session.commit()
    flash('Plato eliminado!', category='success')
    return redirect(url_for('my_dishes'))


@app.route('/order-food/<int:dish_id>', methods=['POST'])
@role_required('worker')
def order_food(dish_id):
    #TODO: limitar la cantidad de pedidos que un trabajador puede hacer 
    if current_user.role != 'worker':
        flash('No tienes permiso para realizar esta acción.', 'danger')
        return redirect(url_for('index'))

    dish = Dish.query.get_or_404(dish_id)

    # Validar la fecha seleccionada
    date = request.form.get('date')
    selected_date = datetime.strptime(date, '%Y-%m-%d').date()
    if not (dish.available_start_date <= selected_date <= dish.available_end_date):
        flash('La fecha seleccionada no está dentro del rango establecido por el proveedor.', 'danger')
        return redirect(url_for('available_dishes'))
    
    today = datetime.today().date()
    week_start = today - timedelta(days=today.weekday())  # Lunes
    week_end = week_start + timedelta(days=6)  # Domingo

    if not (week_start <= selected_date <= week_end):
        flash('La fecha seleccionada debe estar dentro de la misma semana.', 'danger')
        return redirect(url_for('available_dishes'))
    
    quantity = request.form.get('quantity', 1, type=int)
    if quantity <= 0:
        flash('La cantidad debe ser mayor a cero.', 'danger')
        return redirect(url_for('available_dishes'))

    location = request.form.get('location')

    
    order = Order(
        dish_id=dish.id,
        worker_id=current_user.id,
        quantity=quantity,
        deliver_to=location,
        date=selected_date
    )
    db.session.add(order)
    db.session.commit()
    print(date)
    flash('¡Pedido realizado exitosamente!', 'success')
    return redirect(url_for('available_dishes'))


@app.route('/manage_orders', methods=['GET', 'POST'])
@role_required('provider')
def manage_orders():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        new_status = request.form.get('status')
        order = Order.query.get(order_id)

        if order and order.dish.provider_id == current_user.id:
            order.status = new_status
            db.session.commit()
            flash('Estado actualizado correctamente', 'success')
        else:
            flash('Orden no encontrada o no autorizada', 'danger')

        return redirect(url_for('manage_orders'))

    # Obtener órdenes del proveedor actual
    provider_dishes = Dish.query.filter_by(provider_id=current_user.id).all()
    orders = Order.query.join(Dish).filter(Dish.provider_id == current_user.id).all()

    return render_template('manage_orders.html', orders=orders)


@app.route('/worker_orders')
@role_required('worker')
def worker_orders():
    # Obtener las órdenes solicitadas por el trabajador actual
    orders = Order.query.filter_by(worker_id=current_user.id).all()

    return render_template('worker_orders.html', orders=orders)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.route('/unauthorized')
def unauthorized():
    flash('No tienes acceso a la url', category="info")
    return render_template('unauthorized.html')

@app.route('/generate-report', methods=['GET'])
@login_required
def generate_report():
    ROLES_REQUIRED = ['admin', 'finance']
    if current_user.role not in ROLES_REQUIRED:
        flash("No tienes permiso para acceder a esta página.", "danger")
        return redirect(url_for('index'))
    
    provider_id = request.args.get('provider_id')  # Obtener el ID del proveedor de los parámetros de la URL
    if not provider_id:
        return {"error": "provider_id es requerido"}, 400

    start_of_week, today = get_week_range()
    
    # Filtrar órdenes por proveedor y rango de fechas y status
    orders = Order.query.join(Dish).filter(
        Dish.provider_id == provider_id,  # Accede al provider_id a través de la relación Dish
        Order.date >= start_of_week,
        Order.date <= today,
        Order.status == 'aprobada'
    ).all()

    if not orders:
        flash('No hay órdenes para este proveedor en el rango de fechas', category='info')
        return redirect(url_for('list_providers'))

    # Preparar datos para pandas, incluyendo el precio por cantidad
    data = {
        "Pedido ID": [order.id for order in orders],
        "Trabajador": [order.worker.name for order in orders],
        "Proveedor": [order.dish.food_post.name for order in orders],
        "Fecha": [order.date for order in orders],
        "Cantidad": [order.quantity for order in orders],
        "Ubicación": [order.deliver_to for order in orders],
        "Precio por unidad": [order.dish.price for order in orders],  # Precio por unidad
        "Total por orden": [order.quantity * order.dish.price for order in orders],  # Calcular el total por cada orden
    }
    
    # Crear DataFrame con pandas
    df = pd.DataFrame(data)

    # Calcular el total general
    total_price = df['Total por orden'].sum()  # Usar el total por orden para sumar
    total_row = {
        "Pedido ID": "TOTAL",
        "Fecha": "",
        "Cantidad": "",
        "Ubicación": "",
        "Precio por unidad": "",
        "Total por orden": total_price,
    }
    
    # Usar pd.concat para agregar la fila total
    df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

    # Crear archivo temporal en una carpeta válida para Windows
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
        report_file = temp_file.name
        df.to_excel(report_file, index=False, engine='openpyxl')

    # Enviar archivo como descarga
    return send_file(report_file, as_attachment=True, download_name=f"reporte_{start_of_week}_a_{today}.xlsx")

@app.route('/list_providers', methods=['GET'])
@role_required('admin')
def list_providers():
    if current_user.role != 'admin':
        flash("No tienes permiso para acceder a esta página.", "danger")
        return redirect(url_for('index'))

    # Filtrar todos los proveedores
    providers = User.query.filter_by(role='provider').all()

    return render_template('list_providers.html', providers=providers)


@app.route('/validar_usuario/<int:user_id>', methods=['POST'])
@role_required('admin')
def validar_usuario(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('unauthorized'))

    user = User.query.get(user_id)
    user.is_validated = True
    db.session.commit()
    flash(f'Usuario {user.name} validado y activado', 'success')
    return redirect(url_for('admin_dashboard'))
    

@app.route('/revocar_usuario/<int:user_id>', methods=['POST'])
@role_required('admin')
def revocar_usuario(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('unauthorized'))
    user = User.query.get(user_id)
    user.is_validated = False
    db.session.commit()
    flash(f'Usuario {user.name} revocado', 'success')
    return redirect(url_for('admin_dashboard'))
