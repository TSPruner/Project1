import os
import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "QKLXBkeDmu9T5wQluz9LTA", "isbns": "9781632168146"})
print(res.json())

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET", "POST"])
def login():
    print(f"login")
    if request.method == "POST":
        try:
            username = (request.form.get("username"))
        except ValueError:
            return render_template("error.html", message="Invalid or blank username.")

        try:
            password = (request.form.get("password"))
        except ValueError:
            return render_template("error.html", message="Invalid or blank password.")

        print(f"login POST username { username }")
        print(f"login POST password { password }")        
        # Make sure the user exists.
        users = db.execute("SELECT * FROM users WHERE username = :username", {"username": username})
        existingUsers = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username})
        row = existingUsers.fetchone()

        if row is None:
            print(f"user does not exist")
            return render_template("errorLogin.html", message="User does not exist, please register.")

        if row.password == password:
            session["key"] = row.userid
            print(f"row { row.userid }")
            print(f"login call viewUserInfo")
            return render_template("viewUserInfo.html", user=row)
        else:
            print(f"login call errorLogin")
            return render_template("errorLogin.html", message="Password is incorrect, please register.")
        print(f"why here?")

    else:
        print(f"login GET")
        return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        firstname = (request.form.get("first"))
        lastname = (request.form.get("last"))

        try:
            name = (request.form.get("username"))
        except ValueError:
            return render_template("error.html", message="Invalid or blank username.")

        try:
            pswd = (request.form.get("password"))
        except ValueError:
            return render_template("error.html", message="Invalid or blank password.")
        
        # Make sure the user does not exist.
        users = db.execute("SELECT * FROM users WHERE username = :username", {"username": name})
        row = users.fetchone()
        if row is not None:
            return render_template("errorLogin.html", message="Username already exists - please try again.")

        db.execute("INSERT INTO users (username, password, first, last) VALUES (:username, :password, :first, :last)",
                {"username": name, "password": pswd, "first": firstname, "last": lastname})
        newUsers = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": name})
        row = newUsers.fetchone()
            
        db.commit()

        return render_template("successLogin.html")

    else:
        return render_template("registration.html")

@app.route("/viewUserInfo")
def viewUserInfo():
    existingUser = db.execute("SELECT * FROM users WHERE userid = :id",
                        {"id": session["key"]})
    row = existingUser.fetchone()

    print(f"call viewUserInfo")    
    return render_template("viewUserInfo.html", user=row)       

@app.route("/updateUser", methods=["GET", "POST"])
def updateUser():
    print(f"updateUser")
    if request.method == "POST":
        print(f"updateUser POST")

        firstname = (request.form.get("first"))
        lastname = (request.form.get("last"))
        pswd = (request.form.get("password"))

        # Update the user info.
        if (len(firstname) > 0): 
            db.execute("UPDATE users SET first = :first WHERE userid = :id",
                        {"first": firstname, "id": session["key"]})        
        if (len(lastname) > 0):    
            db.execute("UPDATE users SET last = :last WHERE userid = :id",
                        {"last": lastname, "id": session["key"]})
        if (len(pswd) > 0): 
            db.execute("UPDATE users SET password = :pswd WHERE userid = :id",
                       {"pswd": pswd, "id": session["key"]})
        existingUsers = db.execute("SELECT * FROM users WHERE userid = :id",
                        {"id": session["key"]})
        row = existingUsers.fetchone()
        db.commit()

        return render_template("viewUserInfo.html", user=row)

    else:
        print(f"updateUser GET")
        existingUsers = db.execute("SELECT * FROM users WHERE userid = :id",
                        {"id": session["key"]})
        row = existingUsers.fetchone()
        return render_template("updateUser.html", user=row)

@app.route("/searchBooks", methods=["GET", "POST"])
def searchBooks():
    print(f"searchBooks")
    if request.method == "POST":
        print(f"searchBooks POST")

        isbn = (request.form.get("isbn"))
        title = (request.form.get("title"))
        author = (request.form.get("author"))

        # Find books based on data entered.
        if (len(isbn) > 0): 
            if (len(title) > 0):
                if (len(author) > 0):
                    results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND "
                                    "(title LIKE :title OR upper(title) LIKE :title OR lower(title) LIKE :title) AND "
                                    "(author LIKE :author OR upper(title) LIKE :author OR lower(author) LIKE :author)",
                                    {"isbn": "%" + isbn + "%", "title": "%" + title + "%", "author": "%" + author + "%"})
                    foundBooks = results.fetchall()
                    db.commit()
                else:
                    results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND "
                                    "(title LIKE :title OR upper(title) LIKE :title OR lower(title) LIKE :title)",
                                    {"isbn": "%" + isbn + "%", "title": "%" + title + "%"})
                    foundBooks = results.fetchall()
                    db.commit() 
            else:
                results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn",
                                {"isbn": "%" + isbn + "%"})
                foundBooks = results.fetchall()
        elif (len(title) > 0):    
            if (len(author) > 0):
                results = db.execute("SELECT * FROM books WHERE "
                                "(title LIKE :title OR upper(title) LIKE :title OR lower(title) LIKE :title) AND "
                                "(author LIKE :author OR upper(title) LIKE :author OR lower(author) LIKE :author)",
                                {"title": "%" + title + "%", "author": "%" + author + "%"})
                foundBooks = results.fetchall()
            else:
                results = db.execute("SELECT * FROM books WHERE (title LIKE :title OR upper(title) LIKE :title OR lower(title) LIKE :title)",
                                {"title": "%" + title + "%"})
                foundBooks = results.fetchall()
        elif (len(author) > 0): 
            results = db.execute("SELECT * FROM books WHERE (author LIKE :author OR upper(title) LIKE :author OR lower(author) LIKE :author)",
                            {"author": "%" + author + "%"})
            foundBooks = results.fetchall()
        else:
            foundBooks = []

        # Make sure books are found.
        if (len(foundBooks) > 0):
            print(f"searchBooks call findBooks")
            return render_template("findBooks.html", books=foundBooks)
        else:
            return render_template("errorBooks.html", message="No books found, please try again.")

    else:
        print(f"searchBooks GET")
        return render_template("searchBooks.html")

@app.route("/findBooks", methods=["POST"])
def findBooks():
    print(f"findBooks")

    try:
        bookID = int(request.form.get("bookChoice"))
    except ValueError:
        return render_template("error.html", message="Invalid selection.") 

    # Get book info.
    bookSelected = db.execute("SELECT * FROM books WHERE bookid = :id",
                    {"id": bookID})
    bookRow = bookSelected.fetchone()

    # Make sure books are found.
    if (len(bookRow) <= 0):
        db.commit()
        return render_template("errorBooks.html", message="No books found, please try again.")

    # Get review info for book.
    reviewSelected = db.execute("SELECT * FROM reviews WHERE bookid = :id",
                    {"id": bookID})
    reviews = reviewSelected.fetchall()
    userList = []
    print(f"review = {reviews}")

    # Make sure reviews are found.
    if (len(reviews) > 0):
        for row in reviews:
            # Get user's name for review.
            userInfo = db.execute("SELECT * FROM users WHERE userid = :id",
                            {"id": row.userid})
            user = userInfo.fetchone()

            # Make sure user is found.
            if user is None:
                print("No user found")
                return 

            userList.append(user)

    print(f"findbooks call viewBookInfo")
    return render_template("viewBookInfo.html", book=bookRow, reviews=reviews, users=userList)

@app.route("/viewBookInfo", methods=["GET", "POST"])
def viewBookInfo():
    print(f"viewBookInfo")
    return render_template("viewBookInfo.html", book=bookRow, reviews=reviews, users=userList)

@app.route("/findBooks/<int:book_id>")
def reviewBook(book_id):
    print(f"reviewBook")
    userid = session["key"]

    reviewFound = db.execute("SELECT * FROM reviews WHERE userid = :userid AND bookid = :bookid",
            {"userid": userid, "bookid": book_id})
    review = reviewFound.fetchone()

    print(f"review = {review}")
    if review is not None:
        print(f"reviews not empty")
        return render_template("errorBooks.html", message="Book has already been reviewed by user. Please find another book to review.")

    print(f"reviews empty")
    ratings = ["Bad", "Alright", "Good", "Great", "Amazing"]
    return render_template("review.html", bookid=book_id, ratings=ratings)

@app.route("/review/<int:book_id>", methods=["POST"])
def review(book_id):
    print(f"review POST")
    userid = session["key"]

    try:
        rating = request.form.get("rating")
    except ValueError:
        return render_template("error.html", message="Invalid or blank rating.")        

    try:
        comment = request.form.get("comment")
    except ValueError:
        return render_template("error.html", message="Invalid or blank comment.")        

    print(f"rating: {rating}")
    print(f"comment: {comment}")

    # Save the review.
    if (len(comment) > 0): 
        db.execute("INSERT INTO reviews (rating, comment, bookid, userid) VALUES (:rating, :comment, :bookid, :userid)",
            {"rating": rating, "comment": comment, "bookid": book_id, "userid": userid})
        db.commit()

    print(f"reviews")
    return render_template("successReview.html")

@app.route("/logout")
def logout():
    session["key"] = None
    return render_template("successLogout.html")