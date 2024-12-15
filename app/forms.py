from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, ValidationError, RadioField, FloatField, FileField, SelectField, IntegerRangeField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, NumberRange
from app.models import User, Employee

class RegisterForm(FlaskForm):
    """
    Formulario para registrar un nuevo usuario
    """

    def validate_email(self, email_to_check):

        email_address = User.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError('El correo electrónico ya existe! Intenta con otro')

    def validate_national_id(self, national_id_to_check):
        # Verificar si el national_id está en la tabla Employee
        employee = Employee.query.filter_by(national_id=national_id_to_check.data).first()
        if not employee:
            raise ValidationError('La cédula no está registrada como empleado.')

        # Opcional: Validar si ya está registrado en la tabla de usuarios
        user = User.query.filter_by(national_id=national_id_to_check.data).first()
        if user:
            raise ValidationError('Este número de cédula ya está registrado como usuario.')

    name      = StringField(label='Nombre completo:', validators=[Length(min=2, message="El nombre debe tener mas de 2 letras"), DataRequired()])
    national_id = StringField('Cédula de identidad', validators=[DataRequired(), Length(min=7, max=10)])
    email = StringField(label='Correo electrónico:', validators=[Email(message="Por favor ingresa un email valido"), DataRequired()])
    password1     = PasswordField(label='Contraseña:', validators=[Length(min=6), DataRequired()]) 
    password2     = PasswordField(label='Confirmar contraseña:', validators=[EqualTo('password1'), DataRequired()])
    role = RadioField('Departamento:', validators=[DataRequired()], choices=[('worker','Trabajador'),('provider','Proveedor'), ('admin', 'Admin')])
    submit        = SubmitField(label='Crear cuenta')

class LoginForm(FlaskForm):
    """
    Formulario para iniciar sesión
    """
    email=EmailField('Correo electrónico:', validators=[DataRequired()])
    password=PasswordField('Contraseña:', validators=[DataRequired()])
    submit = SubmitField(label='Iniciar sesión')

class DishForm(FlaskForm):
    """
    Formulario para publicar un nuevo plato de comida
    """
    name      = StringField(label='Nombre completo:', validators=[Length(min=2, message=None), DataRequired()])
    description = StringField(label='Escribe detalles de la comida: ')
    price = FloatField(label="Precio:", validators=[DataRequired(), NumberRange(min=0.01, message="El precio debe ser mayor a 0")])
    image_file = FileField(label="Selecciona una imagen:")
    available_start_date = DateField(label="Fecha de inicio disponible:", validators=[DataRequired()])
    available_end_date = DateField(label="Fecha de fin disponible:", validators=[DataRequired()])
    submit = SubmitField(label='Enviar')

class ChangePasswordForm(FlaskForm):
    """
    Formulario para cambiar contraseña
    """
    current_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirmar Nueva Contraseña', validators=[DataRequired(), EqualTo('new_password', message='Las contraseñas deben coincidir.')])
    submit = SubmitField('Cambiar Contraseña')

class AddEmployeeForm(FlaskForm):
    def validate_national_id(self, national_id_to_check):
        # Opcional: Validar si ya está registrado en la tabla de usuarios
        employee = Employee.query.filter_by(national_id=national_id_to_check.data).first()
        if employee:
            raise ValidationError('Este número de cédula ya está registrado como empleado.')

    name      = StringField(label='Nombre completo:', validators=[Length(min=2, message="El nombre debe tener mas de 2 letras"), DataRequired()])
    national_id = StringField('Cédula de identidad', validators=[DataRequired(), Length(min=7, max=10)])
    submit = SubmitField('Crear Empleado')