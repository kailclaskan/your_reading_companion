# Your Reading Companion
### URL: <https://your-reading-companion.herokuapp.com/>

### Description:  
My site utilizes the google books API to allow users to search for a book that they've read, add it to their personal libraries, write a review on it and start a book club on specific subjects in regard to these books. The site allows users to create their own account and reset their password based on information they provide. The user will also be allowed to remove books from their personal libraries, remove their own comments from book clubs and if they created the club they have complete control over the clubs comments and existence. Users who create book clubs, in other words, can remove them from the book club from the system completely, as well as any comments that they feel are too off point/offensive. The database for the books in the library is filled by users searching for, and subsequently viewing the details of, books. It's like facebook/twitter specifically for books.

### Features:  
Users are able to be created and logged in/out. Passwords for users can be reset after verification. Books can be reviewed and users can start book clubs to add to a books information, or just discuss things in regard to a book. Users personal libraries can have books added to and removed from. Users have the ability to add clubs to the system and moderate the conversation. It's fully on the club owner to remove comments and the club itself if they need to. 

### Flow:  
User lands on the Home Page -> User views Your Reading Companion's Library and Clubs. -> User Attempts to review, comment, or create a book club and is redirected to Log In page. -> User then Logs In or Signs Up. -> User adds books to personal library, or views details on books. -> User can then write reviews or create book clubs. They can also interact with created book clubs and comment on them. -> User logs out and is thanked for visiting.
**User forgets password. -> On login page selects Forgot Password button. -> Then the user is able to input Username, Email address and Date of Birth. -> Data is confirmed and the user is given the option of resetting their password if the info checks out. -> They will then need to login with the updated password. 
IF the information doesn't match... -> The user is told that the information isn't correct and redirected to the Sign Up page.

### API:  
Google Books API: <https://developers.google.com/books/docs/overview>.

### Stack:  
- HTML5
- CSS3
- Javascript
- Axios
- Python
- Flask
- PostgreSQL
- SQLAlchemy
- Bcrypt/Flask-Bcrypt
