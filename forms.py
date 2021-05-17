from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=8, max=30),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=15)])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Login')