from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=15),
                                Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                message="Username can't start with space")])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 Length(min=8, max=30),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=2, max=15),
                                Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                message="Username can't start with space")])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8, max=30)])
    submit = SubmitField('Login')


class AddReviewForm(FlaskForm):
    brand_name = StringField(
            'Brand Name', validators=[DataRequired(), Length(min=1, max=30),
                                      Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                      message="Brand name can't start with"
                                      "space")])
    product_review = TextAreaField(
            'Product Review', validators=[DataRequired(),
                                          Length(min=10, max=2000),
                                          Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                          message="Product review can't start"
                                          "with space")])