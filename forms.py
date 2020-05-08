from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, Form
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class SignupForm(FlaskForm):
    """User Signup Form."""
    full_name = StringField('full_name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired(),Length(min=6, message='username should have more thant 6 car.'),DataRequired()])
    email = StringField('Email', validators=[Length(min=6),Email(message='Enter a valid email.'),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, message='Select a stronger password.')])
    confirm = PasswordField('Confirm Your Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm): # <<-- was Form   I change it to Flask Form
    """User Login Form."""
    email = StringField('Email', validators=[DataRequired(), Email(message='Enter a valid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SearchForm(FlaskForm):
    search = StringField('search')
    #NOTE:ADDED: Added "category" to search for a title,isbn,author...etc.
    #    :** Take a look at search.html template.
    #TODO: You still will need to write the codes to distingish your book search.
    #       
    category = StringField('category')
    submit = SubmitField('search')

'''
class searchForm(FlaskForm):
    """User Login Form."""
    search = StringField('search', validators=[DataRequired(), search(message='title, year, author or isbn.')])
    submit = SubmitField('search')
'''
