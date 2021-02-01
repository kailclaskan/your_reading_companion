"""The 'Your Reading Companion' app."""
import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from requests.api import post
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Book, Author, User, User_Library, Author_Work, Book_Club, Book_Club_Comment, Book_Review
from forms import UserSignupForm, UserSignInForm, PostForm, CommentForm, SearchForm, ReviewForm, EditForm
from terrible_secret import secret_key, nyt_api
from genres import genres
from functions import CURR_USER_KEY, check, add_user, add_post, library_check, load_top_20, do_logout, sign_in, library_check, approve, denied



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
    reviews = []
    clubs = []
    book = Book.query.get_or_404(book_id)
    author = Author.query.get_or_404(book.author_id)
    rev = Book_Review.query.filter_by(book_id=book_id, reviewed=True)
    clu = Book_Club.query.filter_by(book_id=book_id, reviewed=True)
    for review in rev:
        reviews.append(review)
    for club in clu:
        clubs.append(club)
    return render_template('book/details.html', book=book, author=author, reviews=reviews, clubs=clubs)

@app.route('/books/check/<book_title>')
def check_book(book_title):
    """
        Verifies if a book is in the database.
        IF not then it adds the book to the database.
        IF it is then it redirects to the books detail page.
    """
    return check(book_title)

@app.route('/books/<int:book_id>/add-review', methods=["GET", "POST"])
def add_review(book_id):
    """Adds a review to a book."""
    form = ReviewForm()
    book = Book.query.get_or_404(book_id)
    if form.validate_on_submit():
        user_review = Book_Review(
            user_id=g.user.id,
            book_id=book_id,
            title=form.headline.data,
            rating=form.rating.data,
            review=form.review.data,    
        )
        db.session.add(user_review)
        db.session.commit() 
        return redirect(f'/books/{book_id}')
    else:
        return render_template("book/book_review.html", form=form, book=book)

########################################################################
###########################Club Related#################################
########################################################################
@app.route('/bookclub')
def clubs():
    """
        The main page for the clubs.
        Will show the most recent activity.
    """
    clubs = Book_Club.query.order_by(desc(Book_Club.discussion_posted_date)).limit(5).all()
    return render_template('book_club/book_club.html', clubs=clubs)

@app.route('/bookclub/<int:book_id>/post', methods=["GET","POST"])
def bookclub_post_form(book_id):
    """The form to make a post in regard to a book."""
    form = PostForm()
    book = Book.query.get_or_404(book_id)
    booktitle = book.title
    if form.validate_on_submit():
        post_title = form.title.data
        post_body = form.body.data
        return add_post(booktitle, post_title, post_body)
    else:
        return render_template('book_club/book_club_post.html', form=form, book=book)

########################################################################
##########################Admin Related#################################
########################################################################

@app.route('/admin')
def admin_home():
    """Directs and admin level user to the administrative tools."""
    all_reviews = Book_Review.query.filter_by(reviewed=False)
    reviews = []
    for review in all_reviews:
        reviews.append(review)
    all_requests = Book_Club.query.filter_by(reviewed=False)
    requests = []
    for request in all_requests:
        requests.append(request)
    comments = []
    all_comments = Book_Club_Comment.query.filter_by(reviewed=False)
    for comment in all_comments:
        comments.append(comment)
    num_reviews = len(reviews)
    num_requests = len(requests)
    num_comments = len(comments)
    return render_template('admin/admin_home.html', num_reviews=num_reviews, num_requests=num_requests, num_comments=num_comments)

@app.route('/admin/admin_reviews')
def admin_reviews():
    """Allows an admin user to approve or deny reviews."""
    reviews = []
    admin_reviews = Book_Review.query.filter_by(reviewed=False)
    for review in admin_reviews:
        reviews.append(review)
    return render_template('admin/admin.html', reviews=reviews)

@app.route('/admin/admin_reviews/<int:request_id>/approved')
def review_approve(request_id):
    """Approves a user's requested change"""
    approve(Book_Review, request_id)
    return redirect('/admin')

@app.route('/admin/<int:request_id>/denied')
def admin_denied(request, request_id):
    """Denies a user's requested change"""

@app.route('/admin/admin_club_comments')
def admin_club_comments():
    """Allows an admin user to approve or deny club comments."""
    comments = []
    admin_comments = Book_Club_Comment.query.filter_by(reviewed=False)
    for comment in admin_comments:
        comments.append(comment)
    return render_template('admin/admin.html', comments=comments)

@app.route('/admin/admin_club_comments/<int:request_id>/approved')
def comment_approve(request_id):
    """Approves a user's requested change"""
    approve(Book_Club_Comment, request_id)
    return redirect('/admin')

@app.route('/admin/admin_club_requests')
def admin_club_requests():
    """Allows an admin user to approve or deny new clubs."""
    clubs = []
    admin_clubs = Book_Club.query.filter_by(reviewed=False)
    for club in admin_clubs:
        clubs.append(club)
    return render_template('admin/admin.html', clubs=clubs)

@app.route('/admin/admin_club_requests/<int:request_id>/approved')
def club_approve(request_id):
    """Approves a user's requested change"""
    approve(Book_Club, request_id)
    return redirect('/admin')

@app.route('/admin/admin_user_updates')
def admin_user_updates():
    """Allows an admin user to reset passwords for users, remove users, and update user data."""
    users = []
    admin_users = User.query.all()
    for user in admin_users:
        users.append(user)
    return render_template('admin/admin.html', users=users)