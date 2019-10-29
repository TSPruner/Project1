import os
import requests

from flask import Flask, session, render_template, jsonify, request
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
    if request.method == "POST":
        try:
            username = (request.form.get("username"))
        except ValueError:
            return render_template("errorLogin.html", message="Invalid or blank username.")

        try:
            password = (request.form.get("password"))
        except ValueError:
            return render_template("errorLogin.html", message="Invalid or blank password.")
      
        # Make sure the user exists.
        existingUsers = db.execute("SELECT * FROM users WHERE username = :username",
                            {"username": username})
        row = existingUsers.fetchone()

        if row is None:
            return render_template("errorLogin.html", message="User does not exist, please register.")

        if row.password == password:
            session["key"] = row.userid
            return render_template("searchBooks.html")
        else:
            return render_template("errorLogin.html", message="Password is incorrect, please register.")

    else:
        return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":

        firstname = (request.form.get("first"))
        lastname = (request.form.get("last"))

        try:
            name = (request.form.get("username"))
        except ValueError:
            return render_template("errorLogin.html", message="Invalid or blank username.")

        try:
            pswd = (request.form.get("password"))
        except ValueError:
            return render_template("errorLogin.html", message="Invalid or blank password.")
        
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
 
    return render_template("viewUserInfo.html", user=row)       

@app.route("/updateUser", methods=["GET", "POST"])
def updateUser():
    if request.method == "POST":

        firstname = (request.form.get("first"))
        lastname = (request.form.get("last"))

        # Update the user info.
        if (len(firstname) > 0): 
            db.execute("UPDATE users SET first = :first WHERE userid = :id",
                        {"first": firstname, "id": session["key"]})        
        if (len(lastname) > 0):    
            db.execute("UPDATE users SET last = :last WHERE userid = :id",
                        {"last": lastname, "id": session["key"]})
        existingUsers = db.execute("SELECT * FROM users WHERE userid = :id",
                        {"id": session["key"]})
        row = existingUsers.fetchone()
        db.commit()

        return render_template("viewUserInfo.html", user=row)

    else:
        existingUsers = db.execute("SELECT * FROM users WHERE userid = :id",
                        {"id": session["key"]})
        row = existingUsers.fetchone()
        return render_template("updateUser.html", user=row)

@app.route("/updatePswd", methods=["GET", "POST"])
def updatePswd():
    if request.method == "POST":

        oldpswd = (request.form.get("oldPassword"))
        newPassword1 = (request.form.get("newPassword1"))
        newPassword2 = (request.form.get("newPassword2"))

        # Check the old password info.
        if (len(oldpswd) > 0):
            existingUsers = db.execute("SELECT * FROM users WHERE userid = :id",
                            {"id": session["key"]})
            row = existingUsers.fetchone()
            if row is None:
                return render_template("errorUser.html", message="Password update failed, please try again")

            # Check the new password info.
            if row.password == oldpswd:
                if (len(newPassword1) > 0) and (len(newPassword2) > 0): 
                    if newPassword1 == newPassword2:
                        db.execute("UPDATE users SET password = :pswd WHERE userid = :id",
                                {"pswd": newPassword1, "id": session["key"]})
                        db.commit()

                        return render_template("successUpdate.html")
                    else:
                        return render_template("errorUser.html", message="New passwords do not match, please try again")
                else:
                    return render_template("errorUser.html", message="Password update failed, please try again")

            return render_template("errorUser.html", message="Old password is incorrect, please try again.")

        return render_template("errorUser.html", message="Password update failed, please try again")

    else:
        # Make sure the user is found.
        existingUsers = db.execute("SELECT * FROM users WHERE userid = :id",
                        {"id": session["key"]})
        row = existingUsers.fetchone()

        if row is None:
            return render_template("errorUser.html", message="User not found, please try again")

        return render_template("updatePswd.html", user=row)

@app.route("/searchBooks", methods=["GET", "POST"])
def searchBooks():
    if request.method == "POST":

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
                else:
                    results = db.execute("SELECT * FROM books WHERE isbn LIKE :isbn AND "
                                    "(title LIKE :title OR upper(title) LIKE :title OR lower(title) LIKE :title)",
                                    {"isbn": "%" + isbn + "%", "title": "%" + title + "%"})
                    foundBooks = results.fetchall()
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
            return render_template("findBooks.html", books=foundBooks)
        else:
            return render_template("errorBooks.html", message="No books found, please try again.")

    else:
        return render_template("searchBooks.html")

@app.route("/findBooks", methods=["POST"])
def findBooks():
    try:
        bookID = int(request.form.get("bookChoice"))
    except ValueError:
        return render_template("errorBook.html", message="Invalid selection.") 

    # Get book info.
    bookSelected = db.execute("SELECT * FROM books WHERE bookid = :id",
                    {"id": bookID})
    bookRow = bookSelected.fetchone()

    # Make sure books are found.
    if bookRow is None:
        db.commit()
        return render_template("errorBooks.html", message="No books found, please try again.")

    # Get review info for book.
    reviewSelected = db.execute("SELECT * FROM reviews WHERE bookid = :id",
                    {"id": bookID})
    reviews = reviewSelected.fetchall()
    userList = []
    goodreadList = []

    # Make sure reviews are found.
    if reviews is not None:
        for row in reviews:
            # Get user's name for review.
            userInfo = db.execute("SELECT * FROM users WHERE userid = :id",
                            {"id": row.userid})
            user = userInfo.fetchone()

            # Make sure user is found.
            if user is not None:
                userList.append(user)

    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "QKLXBkeDmu9T5wQluz9LTA", "isbns": bookRow.isbn})

    if res.status_code != 200:
        goodreadList.append("No goodread review info available at this time.")
    else:
        data = res.json()
        bookdata = data["books"]
        countRating = bookdata[0]["work_ratings_count"]
        avgRating = bookdata[0]["average_rating"]
        goodreadList.append(f"This book received { countRating } reviews and has an average rating of { avgRating } out of 5.")
    
    return render_template("viewBookInfo.html", book=bookRow, reviews=reviews, users=userList, goodreads=goodreadList)

@app.route("/findBooks/<int:book_id>")
def reviewBook(book_id):
    userid = session["key"]

    reviewFound = db.execute("SELECT * FROM reviews WHERE userid = :userid AND bookid = :bookid",
            {"userid": userid, "bookid": book_id})
    review = reviewFound.fetchone()

    if review is not None:
        return render_template("errorBooks.html", message="Book has already been reviewed by user. Please find another book to review.")

    ratings = ["Bad", "Alright", "Good", "Great", "Amazing"]
    return render_template("review.html", bookid=book_id, ratings=ratings)

@app.route("/review/<int:book_id>", methods=["POST"])
def review(book_id):
    userid = session["key"]

    try:
        rating = request.form.get("rating")
    except ValueError:
        return render_template("errorBook.html", message="Invalid or blank rating.")        

    try:
        comment = request.form.get("comment")
    except ValueError:
        return render_template("errorBook.html", message="Invalid or blank comment.")        

    # Save the review.
    if (len(comment) > 0): 
        db.execute("INSERT INTO reviews (rating, comment, bookid, userid) VALUES (:rating, :comment, :bookid, :userid)",
            {"rating": rating, "comment": comment, "bookid": book_id, "userid": userid})
        db.commit()

    return render_template("successReview.html")

@app.route("/logout")
def logout():
    session["key"] = None
    return render_template("successLogout.html")

@app.route("/api/excitingread/<book_isbn>")
def excitingread_api(book_isbn):
    print(f"excitingread_api")

    # Make sure book exists.
    bookFound = db.execute("SELECT * FROM books WHERE isbn = :isbn", 
                    {"isbn": book_isbn})
    row = bookFound.fetchone()

    print(f"row: {row} and isbn = {book_isbn}")
    if row is None:
        print(f"invalid bookisbn")
        return jsonify({"error": "Invalid bookisbn"}), 422

    print(f"isbn valid")

    # Get goodreads info.
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "QKLXBkeDmu9T5wQluz9LTA", "isbns": book_isbn})
    if res.status_code != 200:
        avgRating = 0
        countRating = 0
    else:
        data = res.json()
        print(f"data = { data }")
        bookdata = data["books"]
        countRating = bookdata[0]["work_ratings_count"]
        avgRating = bookdata[0]["average_rating"]
    
    print(f"bookisbn review info: { countRating } and { avgRating }")

    #Return details about an excitingRead book.
    return jsonify({
            "title": row.title,
            "author": row.author,
            "year": row.year,
            "isbn": row.isbn,
            "review_count": countRating,
            "average_score": avgRating
        })

