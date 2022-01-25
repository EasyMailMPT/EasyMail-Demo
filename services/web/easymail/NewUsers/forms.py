from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,IntegerField
from wtforms.validators import DataRequired,Length,Email,EqualTo, ValidationError

from easymail.models import User

class RegistrationForm(FlaskForm):
   
    email = StringField('Email', validators=[DataRequired(),Length(min=4,max=60)])
   
    name = StringField('Name', validators=[DataRequired(),Length(max=20)])
    password = PasswordField('Hasło', validators=[DataRequired(),Length(min=8,max=86,message='Hasło musi mieć przynajmniej: 8 znaków, 1 duza literę i przynajmniej 1 jedną literę')])
    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(),EqualTo('password','Hasła się nie zgadzają')])
   
    submit = SubmitField('Register')
    

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).all()
       
        if user:
            raise ValidationError('Uzytkownik istnieje')

class LoginForm(FlaskForm):
   
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Zapamiętaj mnie')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Poproś o nowe hasło')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Nie ma uztkownika o takim emailu. Zarejestruj się')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zresetuj hasło')
