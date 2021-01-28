from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, validators
from wtforms.fields.core import DateTimeField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UserSignupForm(FlaskForm):
    """Form for users to signup."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=8), 
            validators.EqualTo('password_verifier', 'Passwords must match.')])
    password_verifier = PasswordField(
        'Verify Password', 
        validators=[DataRequired(), Length(min=8)])
    first_name = StringField('User First Name', validators=[DataRequired()])
    last_name = StringField('User Last Name', validators=[DataRequired()])

class UserSignInForm(FlaskForm):
    """Form to login to the site."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class PostForm(FlaskForm):
    """Form to post a Review or Book Club Forum"""
    title = StringField('Title of Post', validators=[DataRequired(), Length(max=120)])
    body = TextAreaField('Post', validators=[DataRequired()])

class CommentForm(FlaskForm):
    """Form to post a comment."""
    body = TextAreaField('Comment', validators=[DataRequired()])

class SearchForm(FlaskForm):
    """The form to search for a book."""
    search = StringField('Search')
    genre = SelectField('Genre')