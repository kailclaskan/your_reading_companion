"""Models for Your Reading Companion"""
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import date


bcrypt = Bcrypt()
db = SQLAlchemy()
d = date.today()
class Book(db.Model):
    """The book class for the database."""

    __tablename__ = 'books'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    title = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('authors.id'),
        nullable=False
    )
    description = db.Column(
        db.Text,
        default='none'
    )
    categories = db.Column(
        db.Text,
        default="Unknown"
    )
    release = db.Column(
        db.Text
    )
    pg_count = db.Column(
        db.Integer
    )
    image = db.Column(
        db.Text,
        default="https://p.kindpng.com/picc/s/494-4945860_cartoon-book-with-blank-cover-printable-blank-book.png"
    )
    isbn = db.Column(
        db.Integer
    )

    library = relationship("User_Library", backref='books')
    club = relationship("Book_Club", back_populates='book')
    review = relationship("Book_Review", back_populates='book')
    author = relationship("Author", back_populates='book')
    
    @classmethod
    def add_book(cls, title, description, author_name, categories, release, image):
        """Adds a book to the database."""
        author = Author.query.filter_by(author_name=author_name).first()

        if author:
            book = Book(
                title=title,
                description=description,
                author_id = author.id,
                categories=categories,
                release=release,
                image=image
            )

            db.session.add(book)
            return book
        else:
            Author.add_author(author_name=author_name)
            db.session.commit()
            author = Author.query.filter_by(author_name=author_name).first()
            book = Book(
                title=title,
                description=description,
                author_id = author.id,
                categories=categories,
                release=release,
                image=image
            )

            db.session.add(book)
            return book
    
class Author(db.Model):
    """The author class defines the author database."""
    
    __tablename__ = 'authors'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    author_name = db.Column(
        db.Text,
        nullable=False
    )
    email = db.Column(
        db.Text
    )
    biography = db.Column(
        db.Text
    )
    
    book = relationship("Book", back_populates="author")

    @classmethod
    def add_author(cls, author_name):
        """Adds an author to the database."""
        author = Author(
            author_name=author_name
        )

        db.session.add(author)
        return author

class User(db.Model):
    """The user class defines the user database."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    username = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    first_name = db.Column(
        db.Text,
        nullable=False
    )
    last_name = db.Column(
        db.Text,
        nullable=False
    )
    email = db.Column(
        db.Text,
        nullable=False
    )
    dob = db.Column(
        db.Text,
        nullable=False
    )
    role = db.Column(
        db.Text,
        nullable=False,
        default="standard_user"
    )

    library = relationship("User_Library", backref="users")
    club = relationship("Book_Club", back_populates="user")
    club_comment = relationship("Book_Club_Comment", back_populates="user")
    review = relationship("Book_Review", back_populates="user")

    @classmethod
    def signup(cls, username, email, password, first_name, last_name, dob):
        """Adds a user to the database."""
        secure_password = bcrypt.generate_password_hash(password, 16).decode('UTF-8')
        secure_dob = bcrypt.generate_password_hash(dob, 14).decode('utf-8')

        user = User(
            username=username,
            email=email,
            password=secure_password,
            first_name=first_name,
            last_name=last_name,
            dob=secure_dob
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Verify the user is who they say they are."""
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return user

    @classmethod
    def forgot(cls, username, email, dob):
        """Checks the user's username, email and dob in case they forget the password to their account."""
        user = cls.query.filter_by(username=username, email=email).first()

        if user:
            correct_birth = bcrypt.check_password_hash(user.dob, dob)
            if correct_birth:
                return user

class User_Library(db.Model):
    """The database to track a users library."""
    __tablename__ = 'user_libraries'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='cascade')
    )
    
    @classmethod
    def add_to_library(cls, user_id, book_id):
        """Adds user_id and book_id to the users library."""
        book = User_Library(
            user_id=user_id,
            book_id=book_id
        )

        db.session.add(book)
        return book
class Author_Work(db.Model):
    """The database holds an authors published works."""
    __tablename__ = 'author_works'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    author_id = db.Column(
        db.Integer,
        db.ForeignKey('authors.id', ondelete='cascade')
    )
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='cascade')
    )

class Book_Club(db.Model):
    """Adds a book club forum to discuss current reading material."""
    __tablename__= 'book_clubs'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='cascade')
    )
    discussion_title = db.Column(
        db.String(120),
        nullable=False
    )
    discussion_body = db.Column(
        db.Text,
        nullable=False
    )
    discussion_posted_date = db.Column(
        db.String(10),
        nullable=False,
        default=date.strftime(d, "%m/%d/%Y")
    )

    book = relationship("Book", back_populates="club")
    user = relationship("User", back_populates="club")
    comments = relationship("Book_Club_Comment", back_populates="club")

    @classmethod
    def post_forum(cls, user_id, book_id, discussion_title, discussion_body):
        """Adds a forum to discuss interests in books."""
        post = Book_Club(
            user_id=user_id,
            book_id=book_id,
            discussion_title=discussion_title,
            discussion_body=discussion_body
        )

        db.session.add(post)
        return post

class Book_Club_Comment(db.Model):
    """Comments on the forum posts."""
    __tablename__ = 'book_club_comments'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True
    )
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('book_clubs.id', ondelete='cascade')
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )
    comment = db.Column(
        db.Text,
        nullable=False
    )
    comment_date = db.Column(
        db.String(10),
        nullable=False,
        default=date.strftime(d, "%m/%d/%Y")
    )

    user = relationship("User", back_populates="club_comment")
    club = relationship("Book_Club", back_populates="comments")

    @classmethod
    def add_comment(cls, comment, post_id, user_id):
        """Adds a comment to a book club forum."""
        comment = Book_Club_Comment(
            post_id=post_id,
            user_id=user_id,
            comment=comment
        )

        db.session.add(comment)
        return comment

class Book_Review(db.Model):
    """
    Add a book review to a book.
    Comments will not be allowed on the reviews.
    """
    __tablename__ = 'book_reviews'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )
    book_id = db.Column(
        db.Integer,
        db.ForeignKey('books.id', ondelete='cascade')
    )
    rating = db.Column(
        db.Integer,
        nullable=False
    )
    title = db.Column(
        db.String(120),
        nullable=False
    )
    review = db.Column(
        db.Text,
        nullable=False
    )
    review_date = db.Column(
        db.String(10),
        nullable=False,
        default=date.strftime(d, "%m/%d/%Y")
    )

    book = relationship("Book", back_populates="review")
    user = relationship("User", back_populates="review")
    
    @classmethod
    def add_review(cls, user_id, book_id, title, rating, review):
        """Adds a review to a book."""
        review = Book_Review(
            user_id=user_id,
            book_id=book_id,
            title=title,
            rating=rating,
            review=review
        )

        db.session.add(review)
        return review

def connect_db(app):
    """Connects Flask app to database."""
    db.app = app
    db.init_app(app)