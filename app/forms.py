from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from sqlalchemy import select
from app import db
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmed_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    photo = FileField('Photo', validators=[DataRequired(), FileAllowed(['png', 'jpg'], 'Only images!')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        with db.session as session:
            user = session.scalar(
                select(User).where(User.username == username.data)
            )
            if user:
                raise ValidationError('Username already exists')

    def validate_email(self, email):
        with db.session as session:
            user = session.scalar(
                select(User).where(User.email == email.data)
            )
            if user:
                raise ValidationError('Email already exists')


    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('password must be longer than 8 symbols')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')