import os

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
    if request.method == "POST":
        try:
            username = int(request.form.get("username"))
        except ValueError:
            return render_template("error.html", message="Invalid or blank username.")

        try:
            password = int(request.form.get("password"))
        except ValueError:
            return render_template("error.html", message="Invalid or blank username.")

        Users = ["Test1", "***", "Tiffany", "Pruner"] 
        return render_template("viewUserInfo.html", Users=Users)

    else:    
        return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    return render_template("registration.html")

@app.route("/viewUserInfo", methods=["GET", "POST"])
def viewUserInfo():
    Users = ["Test1", "***", "Tiffany", "Pruner"]
    return render_template("viewUserInfo.html", Users=Users)

@app.route("/searchBooks", methods=["GET", "POST"])
def searchBooks():
    return render_template("searchBooks.html")

@app.route("/findBooks", methods=["GET", "POST"])
def findBooks():
    Books = ["380795272", "Krondor: The Betrayal", "Raymond E. Feist", 1998]
    ISBN = "380795272"
    return render_template("findBooks.html", Books=Books, ISBN=ISBN)

@app.route("/viewBookInfo", methods=["GET", "POST"])
def viewBookInfo():
    Books = ["380795272", "Krondor: The Betrayal", "Raymond E. Feist", 1998]
    Review1 = [1, 5, "Great Book!", "380795272", "Test1"]
    Review2 = [2, 4, "Really like it", "380795272", "Test2"]
    Reviews = ["00123456", "380795272", "380795272"]
    return render_template("viewBookInfo.html", Books=Books, Review1=Review1, Review2=Review2, Reviews=Reviews)

@app.route("/review", methods=["GET", "POST"])
def review():
    ISBN = "380795272"
    Review = [0, 0, " ", ISBN, "Test1"]
    return render_template("review.html", ISBN=ISBN, Review=Review)

@app.route("/logout")
def logout():
    return render_template("success.html")