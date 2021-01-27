"""The 'Your Reading Companion' app."""
import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Book, Author, User, User_Library, Author_Work, Book_Club, Book_Club_Comment, Book_Review
from secret import secret_key, nyt_api

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///your_reading_companion')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secret_key)
toolbar = DebugToolbarExtension(app)

connect_db(app)

######################################################################
###############################Routes#################################
######################################################################
@app.route('/')
def index():
    """Redirects to the home page"""
    top_rated = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/best-sellers.json?api-key={nyt_api}')
    print('hello')
    results = top_rated.json().get('results', [])
    return render_template('index.html', results=results)