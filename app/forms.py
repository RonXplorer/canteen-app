from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, ValidationError, RadioField, FloatField, FileField, SelectField, IntegerRangeField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, NumberRange
from app.models import User

class RegisterForm(FlaskForm):

    def validate_email(self, email_to_check):

        email_address = User.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError('El correo electrónico ya existe! Intenta con otro')

    name      = StringField(label='Nombre completo:', validators=[Length(min=2, message=None), DataRequired()])
    email = StringField(label='Correo electrónico:', validators=[Email(), DataRequired()])
    password1     = PasswordField(label='Contraseña:', validators=[Length(min=6), DataRequired()]) 
    password2     = PasswordField(label='Confirmar contraseña:', validators=[EqualTo('password1'), DataRequired()])
    role = RadioField('Departamento:', validators=[DataRequired()], choices=[('worker','Trabajador'),('provider','Proveedor'), ('admin', 'Admin')])
    submit        = SubmitField(label='Crear cuenta')

class LoginForm(FlaskForm):
    email=EmailField('Correo electrónico:', validators=[DataRequired()])
    password=PasswordField('Contraseña:', validators=[DataRequired()])
    submit = SubmitField(label='Iniciar sesión')

class DishForm(FlaskForm):
    name      = StringField(label='Nombre completo:', validators=[Length(min=2, message=None), DataRequired()])
    description = StringField(label='Escribe detalles de la comida: ')
    price = FloatField(label="Precio:", validators=[DataRequired(), NumberRange(min=0.01, message="El precio debe ser mayor a 0")])
    image_file = FileField(label="Selecciona una imagen:")
    available_start_date = DateField(label="Fecha de inicio disponible:", validators=[DataRequired()])
    available_end_date = DateField(label="Fecha de fin disponible:", validators=[DataRequired()])
    submit = SubmitField(label='Enviar')