"""The 'Your Reading Companion' app."""
import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Book, Author, User, User_Library, Author_Work, Book_Club, Book_Club_Comment, Book_Review
from forms import UserSignupForm, UserSignInForm, PostForm, CommentForm, SearchForm
from terrible_secret import secret_key, nyt_api
from genres import genres
from functions import CURR_USER_KEY, check, add_user, add_post, library_check, load_top_20, do_logout, sign_in, library_check



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
##########################Base Routes#################################
######################################################################
@app.before_request
def add_user_to_g():
    """If logged in add current user to the global g"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None
        
@app.route('/')
def index():
    """Redirects to the home page"""
    results = load_top_20()
    return render_template('index.html', results=results)


########################################################################
###########################User Related#################################
########################################################################
@app.route('/users/signup', methods=["GET", "POST"])
def user_signup():
    """Signs a user up."""
    return add_user()

@app.route('/users/signin', methods=["GET", "POST"])
def user_signin():
    """Signs a user into their account."""
    return sign_in()

@app.route('/users/signout')
def user_signout():
    """Signs a user out."""
    return do_logout()

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Shows the user's detail page."""
    #Need to create a relationship between book and author so I can pull author without too much stress.
    library = User_Library.query.filter_by(user_id=user_id)
    clubs = Book_Club.query.filter_by(user_id=user_id)
    books = []
    for book in library:
        book_q = Book.query.get(book.book_id)
        books.append(book_q)
    return render_template('user/user_page.html', books=books, clubs=clubs)

@app.route('/users/<int:user_id>/library/check/<title>')
def add_to_users_library(user_id, title):
    """Checks a users library for if this book exists."""
    return library_check(user_id, title)

@app.route('/users/<int:user_id>/library/remove/<book_id>')
def remove_book_from_user_library(user_id, book_id):
    """Removes a book from the users library."""
    book = User_Library.query.filter_by(user_id=user_id, book_id=book_id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/search/<username>')
def search_user(username):
    """Finds the logged userid for js."""
    user = User.query.filter_by(username=username).first()
    id = f'{user.id}'
    return id

########################################################################
###########################Book Related#################################
########################################################################
@app.route('/books', methods=["GET", "POST"])
def books_home():
    """This loads the search criteria for finding books."""
    if g.user:
        form = SearchForm()
        form.genre.choices = [genre for genre in genres]
        return render_template('book/all_books.html', form=form)
    else:
        flash("Must be logged in to view that page.", "warning")
        return redirect('/users/signin')

@app.route('/books/<int:book_id>')
def book_info(book_id):
    """This loads info of the selected book."""
    book = Book.query.get_or_404(book_id)
    author = Author.query.get_or_404(book.author_id)
    return render_template('book/details.html', book=book, author=author)

@app.route('/books/check/<book_title>')
def check_book(book_title):
    """
        Verifies if a book is in the database.
        IF not then it adds the book to the database.
        IF it is then it redirects to the books detail page.
    """
    return check(book_title)

########################################################################
###########################Club Related#################################
########################################################################
@app.route('/bookclub')
def clubs():
    """
        The main page for the clubs.
        Will show the most recent activity.
    """
    form = PostForm()
    return render_template('book_club/book_club.html', form=form)

@app.route('/bookclub/post')
def post_to_club():
    """The form to make a post in regard to a book."""
    form = PostForm()

    return render_template('book_club/book_club_post.html', form=form)