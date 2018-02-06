from flask_wtf import FlaskForm
from wtforms   import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email       = StringField('Correo', validators=[
                     InputRequired(message="campo requerido"),
                     Email(message='correo inválido')
                 ])
    password    = PasswordField('Contraseña', validators=[InputRequired(message="campo requerido")])
    remember_me = BooleanField('Recordarme')
    submit      = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username   = StringField('Usuario',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=32, message="el usuario no puede tener más de 32 caracteres")
                 ])
    first_name = StringField('Nombre(s)',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=32, message="el nombre no puede tener más de 32 caracteres")
                 ])
    last_name  = StringField('Apellido(s)',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=32, message="el apellido no puede tener más de 32 caracteres")
                 ])
    email      = StringField('Correo',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Email(message='correo inválido'),
                     Length(max=32, message="el correo no puede tener más de 32 caracteres")
                 ])
    password   = PasswordField('Contraseña',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=32, message="la contraseña debe ser entre 8 y 500 caracteres"),
                     EqualTo('confirm', message='las contraseñas no coinciden')
                 ])
    confirm    = PasswordField('Repetir contraseña',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=32, message="la contraseña debe ser entre 8 y 500 caracteres"),
                 ])
    submit     = SubmitField('Registrarse')

class EditForm(FlaskForm):
    username   = StringField('Usuario',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=32, message="el usuario no puede tener más de 32 caracteres")
                 ])
    email       = StringField('Correo', validators=[
                     InputRequired(message="campo requerido"),
                     Email(message='correo inválido')
                 ])
    about_me   = StringField('Sobre mi',
                 validators=[
                     Length(max=140, message="el campo no puede tener más de 140 caracteres")
                 ])

class PostForm(FlaskForm):
    post       = StringField('Mensaje',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=1000, message="el mensaje debe ser menor a 1000 caracteres")
                 ])
    submit     = SubmitField('Enviar')

class SearchForm(FlaskForm):
    search = StringField('Buscar',
                 validators=[
                     InputRequired(message="campo requerido"),
                     Length(max=1000, message="el patrón de búsqueda debe ser menor a 1000 caracteres")
                 ])
    submit = SubmitField('Buscar')
