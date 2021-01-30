import os
import requests

from flask import Flask, render_template, redirect, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, Book, Author, User, User_Library, Author_Work, Book_Club, Book_Club_Comment, Book_Review
from forms import UserSignupForm, UserSignInForm, PostForm, CommentForm, SearchForm
from terrible_secret import secret_key, nyt_api
from genres import genres

CURR_USER_KEY = 'curr_user'

def add_book(title, info, first_name, last_name):
    """Adds a book to the database."""
    Book.add_book(
            title=title,
            description=info['description'],
            author_first_name=first_name,
            author_last_name=last_name,
            categories=info['categories'],
            release=info['publishedDate'],
            image=info['imageLinks']['thumbnail']
        )

def add_post():
    """"""

def add_to_user_library(user, book):
    """Adds a book to the users library database."""
    User_Library.add_to_library(
        user_id = user.id,
        book_id = book.id
    )

def add_user():
    """Adds a user to the database."""
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

        return redirect(f'/users/{session[CURR_USER_KEY]}')
    else:
        return render_template('user/signup.html', form=form)

def check(book_title):
    """ Checks if a book is in the system. IF it is it redirects to the books detail page.
        IF it isn't it adds it, then redirects to the details page.
    """
    title = filter_word(book_title)
    book = Book.query.filter_by(title=title).first()
    if not book:
        #################################still need to fix the title issue. # seems to be the issue. Need to figure out how to escape the hashtag.
        resp = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title}')
        details = resp.json().get('items', [])
        info = details[0]['volumeInfo']
        author=info['authors'][0]
        if len(author.split(" ")) > 2:
            first_name, middle_name, last_name = author.split(" ")
        else:
            first_name, last_name = author.split(" ")
        title = info['title']
        
        add_book(title, info, first_name, last_name)
        db.session.commit()
        direct = Book.query.filter_by(title=title).first()
        return redirect(f'/books/{direct.id}')
    else:
        return redirect(f'/books/{book.id}')

def do_login(user):
    """User logs in."""
    
    session[CURR_USER_KEY] = user.id

def do_logout():
    """User logout"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        flash("Have a nice day!", "secondary")
        return redirect('/')

def filter_word(word):
    """Removes unwanted characters"""
    unwanted_chars = ['#', '!', ';', '$','\'', '\"', '.']

    for i in unwanted_chars:
        word = word.replace(i, '')

        return word

def library_check(user_id, title):
    """Checks to see if the book is in the users library."""
    book = Book.query.filter_by(title=title).first()
    user = User.query.get(user_id)

    if book:
        in_library = User_Library.query.filter_by(user_id=user.id, book_id=book.id)
        if not in_library:
            add_to_user_library(user, book)
            db.session.commit()
            flash("Book added to your library", "success")
            return redirect('/books')
        else:
            flash("Book already in your library", "info")
            return redirect('/books')
    
    else:
        resp = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title}')
        details = resp.json().get('items', [])
        info = details[0]['volumeInfo']
        author=info['authors'][0]
        #Find a better way to handle the author name.
        if len(author.split(" ")) > 2:
            first_name, middle_name, last_name = author.split(" ")
        else:
            first_name, last_name = author.split(" ")
        
        title = info['title']
        add_book(title, info, first_name, last_name)
        db.session.commit()
        book = Book.query.filter_by(title=title).first()
        add_to_user_library(user, book)
        db.session.commit()
        flash("Book added to your library", "success")
        return redirect('/books')

def load_top_20():
    """
        Loads the top 20 books according to NYT then filters them through the
        google books api to get the details.
    """
    results = []
    top_rated = requests.get(f'https://api.nytimes.com/svc/books/v3/lists/best-sellers.json?api-key={nyt_api}')
    books = top_rated.json().get('results', [])
    for book in books:
        title = book['title']
        title = filter_word(title)
        resp = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={title}')
        result = resp.json().get('items', [])
        results.append(result)
    return results

def sign_in():
    """Signs a user in to a page."""
    form = UserSignInForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Welcome to Your Reading Companion {user.username}", "success")

            return redirect(f'/users/{user.id}')
        else:
            flash("Invalid Sign In.", "danger")
            return render_template('user/signin.html', form=form)
    else:
        return render_template('user/signin.html', form=form)