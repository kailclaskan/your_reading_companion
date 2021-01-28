"""The 'Your Reading Companion' app."""
import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Book, Author, User, User_Library, Author_Work, Book_Club, Book_Club_Comment, Book_Review
from terrible_secret import secret_key, nyt_api
from forms import UserSignupForm, UserSignInForm, PostForm, CommentForm, SearchForm

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///your_reading_companion')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
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

def do_login(user):
    """User logs in."""
    
    session[CURR_USER_KEY] = user.id

def do_logout():
    """User logout"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def index():
    """Redirects to the home page"""
    results = []
    top_rated = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/best-sellers.json?api-key={nyt_api}')
    books = top_rated.json().get('results', [])
    for book in books:
        title = book['title']
        title = filter_word(title)
        resp = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title}')
        result = resp.json().get('items', [])
        results.append(result)
    return render_template('index.html', results=results)


########################################################################
###########################User Related#################################
########################################################################
@app.route('/users/signup', methods=["GET", "POST"])
def user_signup():
    """Signs a user up."""
    form = UserSignupForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('user/signup.html', form=form)
        
        do_login(user)

        return redirect('/')
    else:
        return render_template('user/signup.html', form=form)

@app.route('/users/signin', methods=["GET", "POST"])
def user_signin():
    """Signs a user into their account."""
    form = UserSignInForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Welcome to Your Reading Companion {user.username}", "success")

            return redirect('/')
        else:
            flash("Invalid Sign In.", "danger")
            return render_template('user/signin.html', form=form)
    else:
        return render_template('user/signin.html', form=form)

@app.route('/users/signout')
def user_signout():
    """Signs a user out."""
    do_logout()

    return redirect('/')

@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Shows the user's detail page."""
    user = User.query.get_or_404(user_id)
    books = User_Library.query.filter_by(user_id=user.id)
    return render_template('user/user_page.html', books=books)

########################################################################
###########################Book Related#################################
########################################################################
@app.route('/books', methods=["GET", "POST"])
def books_home():
    """This loads the search criteria for finding books."""

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
    title = filter_word(book_title)
    print(title)
    book = Book.query.filter_by(title=title).first()
    if book:
        return redirect(f'/books/{book.id}')

    else:
        resp = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title}')
        details = resp.json().get('items', [])
        info = details[0]['volumeInfo']
        author=info['authors'][0]
        if len(author.split(" ")) > 2:
            first_name, middle_name, last_name = author.split(" ")
        else:
            first_name, last_name = author.split(" ")
        title = info['title']
        Book.add_book(
            title=title,
            description=info['description'],
            author_first_name=first_name,
            author_last_name=last_name,
            categories=info['categories'],
            release=info['publishedDate'],
            pg_count=info['pageCount'],
            image=info['imageLinks']['thumbnail']
        )
        db.session.commit()
        return redirect('/')

########################################################################
###########################Club Related#################################
########################################################################


########################################################################
##########################Other Functions###############################
########################################################################
def filter_word(word):
    """Removes unwanted characters"""
    unwanted_chars = ['#', '!', ';', '$','\'', '\"']

    for i in unwanted_chars:
        word = word.replace(i, '')

        return word
