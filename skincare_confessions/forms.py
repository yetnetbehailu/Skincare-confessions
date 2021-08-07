from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField,
                     TextAreaField, BooleanField,
                     FloatField, RadioField)
from wtforms.validators import (InputRequired, Length, EqualTo, Regexp,
                                Email)
from flask_wtf.file import FileField, FileAllowed


class RegisterForm(FlaskForm):
    username = StringField(
        'Username', validators=[InputRequired(), Length(min=2, max=15),
                                Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                message="Username can't start with space")])
    password = PasswordField(
        'Password', validators=[InputRequired(), Length(min=8, max=30)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[InputRequired(),
                                                 Length(min=8, max=30),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField(
        'Username', validators=[InputRequired(), Length(min=2, max=15),
                                Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                message="Username can't start with space")])
    password = PasswordField(
        'Password', validators=[InputRequired(), Length(min=8, max=30)])
    submit = SubmitField('Login')


class AddReviewForm(FlaskForm):
    brand_name = StringField(
            'Brand Name', validators=[InputRequired(), Length(min=1, max=15),
                                      Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                                      message="Brand name can't start with"
                                      "space")])
    product_review = TextAreaField(
            'Product Review',
            validators=[InputRequired(), Length(min=10, max=2000),
                        Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                        message="Product review can't start with space")])
    price = FloatField('Price', validators=[InputRequired()])
    is_vegan = BooleanField('Vegan')
    rating = RadioField('Rating', validators=[InputRequired()],
                        choices=[('1', 'Boycott'),
                                 ('2', 'Poor'),
                                 ('3', 'Good'),
                                 ('4', 'Very Good'),
                                 ('5', 'Fantastic')])
    tags = StringField(
        'Tag', validators=[InputRequired(), Length(min=1, max=30),
                           Regexp('^([a-zA-Z0-9-!@#$%^&*])',
                           message="Search tag can't start with space")])
    upload_img = FileField(validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add')
    cancel = SubmitField('Cancel')


class EmailForm(FlaskForm):
    email = StringField(
        'Enter Email...', validators=[InputRequired(), Email()])
    subscribe = SubmitField('Sign up!')
