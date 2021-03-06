from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, validators
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Email, Length

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
    date_of_birth = StringField('Your Date of Birth', validators=[DataRequired()])

class UserSignInForm(FlaskForm):
    """Form to login to the site."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class PostForm(FlaskForm):
    """Form to post to the Book Club Forum"""
    title = StringField('Title of Post', validators=[DataRequired(), Length(max=120)])
    body = TextAreaField('Post', validators=[DataRequired()])

class ReviewForm(FlaskForm):
    """Form to post a Review or Book Club Forum"""
    rating = SelectField('Rating out of 10', choices=[('1','1'), ('2','2'), ('3','3'),('4','4'), ('5','5'),('6','6'),('7','7'), ('8','8'), ('9','9'), ('10','10')])
    headline = StringField('Title of Post', validators=[DataRequired(), Length(max=120)])
    review = TextAreaField('Post', validators=[DataRequired()])

class CommentForm(FlaskForm):
    """Form to post a comment."""
    comment = TextAreaField('Comment', validators=[DataRequired()])

class SearchForm(FlaskForm):
    """The form to search for a book."""
    search = StringField('Search by Title or Author')
    genre = SelectField('Select Genre to Search by')

class ForgotForm(FlaskForm):
    """This form will allow the user to input their email and DOB to reset password."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    dob = StringField('Date of Birth', validators=[DataRequired()])

class ResetForm(FlaskForm):
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(), 
            Length(min=8), 
            validators.EqualTo('password_verifier', 'Passwords must match.')])
    password_verifier = PasswordField(
        'Verify Password', 
        validators=[DataRequired(), Length(min=8)])