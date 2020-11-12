import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime, timedelta
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, weatherapp


app = Flask(__name__)


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///weather.db")

if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        result = weatherapp(request.form.get("location"),None)
        if result["cod"] == "404":
            return apology("No data found for your search request",403)
        url = "http://openweathermap.org/img/wn/"
        sunrise = datetime.fromtimestamp(result["sys"]["sunrise"] + result["timezone"]).time()
        sunset = datetime.fromtimestamp(result["sys"]["sunset"] + result["timezone"]).time()
        duplicate = db.execute("SELECT * FROM 'history' WHERE data_id = :dataid", dataid = result["id"])
        if len(duplicate) != 1:
            db.execute("INSERT INTO 'history' (user_id, data_id) VALUES (:user_id, :data_id)", user_id = session["user_id"], data_id = result["id"])
        return render_template("indexResult.html",result=result, sunrise = sunrise, sunset = sunset, url = url)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    if request.method == "GET":
        sumHistory = []
        history = db.execute("SELECT * FROM 'history' WHERE user_id = :session", session = session["user_id"] )
        for histories in history:
            sumHistory.append(weatherapp(None,histories["data_id"]))
        return render_template("history.html", sumHistory = sumHistory)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        checkUser = db.execute("SELECT * FROM 'users' WHERE username=:username",username=username)
        if not username:
            return apology("please provide a username",403)
        if not password:
            return apology("please provide a password",403)
        if len(checkUser) == 0:
            return apology("username not found, please register first",403)
        if check_password_hash(checkUser[0]["hash"],password) != True:
            return apology("invalid password", 403)
        session["user_id"] = checkUser[0]["id"]
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        checkUser = db.execute("SELECT * FROM 'users' WHERE username=:username",username=username)
        checkEmail = db.execute("SELECT * FROM 'users' WHERE email=:email",email=email)

        if len(checkUser) != 0:
            return apology("Username already exists", 403)
        if len(checkEmail) != 0:
            return apology("Someone already signed up with this email-adress", 403)
        if not username or not email or not password:
            return apology("please provide a username/password and email", 403)
        hash = generate_password_hash(password)
        db.execute("INSERT INTO 'users' (username,hash,email) VALUES (:username, :hash, :email)", username = username, hash = hash, email = email)
        return redirect("/login")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()

    return redirect("/")
