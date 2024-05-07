from flask import Flask, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_caching import Cache 
from cs50 import SQL
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, cache
from luhnchecker.luhn import Luhn
import findMovies

# Configure app
app = Flask(__name__)
db = SQL("sqlite:///users.db")
movie_db = SQL("sqlite:///movies.db")
cache.init_app(app, config={'CACHE_TYPE': 'simple'})
# app.app_context().push()
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=True)
#     password = db.Column(db.String(80), nullable=False)


@app.route("/")
@login_required
def index():
    username = session.get("username")
    popular = findMovies.findPopular(3)
    return render_template("index.html", username=username,popular=popular)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please enter your username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please enter your password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please enter your username")

        if not password:
            return apology("Please enter your password")

        if not confirmation:
            return apology("Please confirm your password")

        if password != confirmation:
            return apology("Confirmation does not match password")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, password) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")
        # session["user_id"] = new_user

        return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")
    else:
        user_id = session.get("user_id")

        password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not password:
            return apology("Please enter your current password")

        if not new_password:
            return apology("Please enter your new password")

        if not confirmation:
            return apology("Please confirm your password")

        if new_password != confirmation:
            return apology("Confirmation does not match password")
        
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], password):
            return apology("Incorrect password", 403)

        hash = generate_password_hash(new_password)
        try:
            db.execute("UPDATE users SET password = ? WHERE id = ?", hash, user_id)
            return render_template("redirect_page.html", alert_message="Password changed. You will be redirected to home page.")
        except Exception as e:
            return apology(str(e))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/find_movie", methods=["GET", "POST"])
@login_required
def find_movie():
    if request.method == "POST":
        movie = request.form.get("movieName")
        results = movie_db.execute("SELECT movies.id, title, year, rating, votes FROM movies LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE title LIKE ? ORDER BY votes DESC LIMIT 8", "%" + movie + "%")
        for result in results:
            result["link"] = findMovies.findPosters(str(result["id"]))
        return render_template("find_movie.html", results=results)
    return render_template("find_movie.html")

@app.route("/profile")
@login_required
def profile():
    user_id = session.get("user_id")
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    return render_template("profile.html", user=user)

@app.route("/upgrade")
@login_required
def upgrade():
    return render_template("upgrade.html")

@app.route("/upgrade_portal", methods=["GET", "POST"])
@login_required
def upgrade_portal():
    if request.method == "POST":
        card_number = request.form.get("card-number-input")
        if Luhn.check_luhn(card_number):
            user_id = session.get("user_id")
            db.execute("UPDATE users SET role = ? WHERE id = ?", "premium", user_id)
            return render_template("redirect_page.html", alert_message="Your account is upgraded. You will be redirected to home page.")
        else:
            return render_template("redirect_page.html", alert_message="Invalid card. You will be redirected to home page.")
    return render_template("credit.html")

@app.route("/movie")
@login_required
def movie():
    movie_id = request.args["movie_id"]
    