from flask import Flask, redirect, render_template, request, flash, session, jsonify
from flask_session import Session
from flask_caching import Cache 
from cs50 import SQL
import json
# from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from luhnchecker.luhn import Luhn
from helpers import apology, login_required, cache
import findMovies

# Configure app
app = Flask(__name__)
db = SQL("sqlite:///users.db")
db.execute("PRAGMA foreign_keys = ON;")
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
    popular = findMovies.findPopular()
    now_playing = findMovies.findNowPlaying()
    top_rated = findMovies.findTopRated()
    upcoming = findMovies.findUpcoming()
    return render_template("index.html", username=username,popular=popular, playing=now_playing, top=top_rated, upcoming=upcoming)


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
        session["role"] = rows[0]["role"]
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
            user_id = db.execute("SELECT * FROM users WHERE username = ?", username)[0]["id"]
            db.execute("INSERT INTO lists (user_id, list_title) VALUES (?, ?)", user_id, "Favourites")
            db.execute("INSERT INTO lists (user_id, list_title) VALUES (?, ?)", user_id, "Watchlist")
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
        results = movie_db.execute("SELECT movies.id, title, year, rating, votes FROM movies LEFT JOIN ratings ON movies.id = ratings.movie_id WHERE title LIKE ? ORDER BY votes DESC LIMIT 10", "%" + movie + "%")
        for result in results:
            movie_detail = findMovies.findPosters(str(result["id"]))
            result["link"] = movie_detail[0]
            result["id"] = movie_detail[1]
        return render_template("find_movie.html", results=results, movie_name=movie)
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
    user_id = session.get("user_id")
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]
    return render_template("upgrade.html", user=user)

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

@app.route("/movie_list", methods=["GET", "POST"])
@login_required
def movie_list():
    user_id = session.get("user_id")
    if request.method == "POST":
        list_name = request.form.get("listName")
        check = db.execute("SELECT * FROM lists WHERE user_id = ? AND list_title = ?", user_id, list_name)
        if len(check) == 0:
            db.execute("INSERT INTO lists (user_id, list_title) VALUES (?, ?)", user_id, list_name)
            flash("List created !", category="success")
        else:
            flash("List name already exists !", category="error")
    user_list = []
    lists = db.execute("SELECT id, list_title FROM lists WHERE user_id = ?", user_id)
    for list in lists:
        film_list = dict()
        list_id = list["id"]
        list_title = list["list_title"]
        film_list["id"] = list_id
        film_list["name"] = list_title
        movies = []
        for id in getMovieinList(list_id):
            movie = {"id": id,
                     "name": db.execute("SELECT * FROM movies WHERE id = ?", id)[0]["movie_name"],
                     "poster": db.execute("SELECT * FROM movies WHERE id = ?", id)[0]["poster"]}
            movies.append(movie)
        
        film_list["movies"] = movies
        
        user_list.append(film_list)

    return render_template("list.html", lists=user_list)
    
@app.route("/movie/")
@login_required
def movie():
    user_id = session.get("user_id")
    movie_id = str(request.args.get("movie_id"))
    images = findMovies.getMoviePicture(movie_id)
    movie_details = findMovies.getMovieDetails(movie_id)
    list_info = db.execute("SELECT * FROM lists WHERE user_id = ?", user_id)
    list_names = [l["list_title"] for l in list_info]
    list_ids = [l["id"] for l in list_info]
    inList = []
    fav = []
    watch = []
    for list in list_ids:
        status = {"list_id": list, "list_name": list_names[list_ids.index(list)], "status": int(movie_id) in getMovieinList(list)}
        if status["list_name"] == "Favourites":
            fav.append(status)
        elif status["list_name"] == "Watchlist":
            watch.append(status)
        else:
            inList.append(status)
    role = db.execute("SELECT * FROM users WHERE id = ?", user_id)[0]["role"]
    clips = findMovies.getMovieClips(movie_id)
    return render_template("movie.html", movie=movie_details, lists=inList, fav=fav[0], watch=watch[0], images=images, role=role, clips=clips)

@app.route("/pictures/")
@login_required
def pictures():
    movie_id = request.args.get("movie_id")
    images = findMovies.getMoviePicture(movie_id)
    return render_template("gallery.html", images=images)

@app.route("/popular/")
@login_required
def popular():
    page = int(request.args.get("page"))
    popular = findMovies.findPopular(page)
    return render_template("category.html", results=popular, page_number=page, pages=list(range(1, 11)), name="Popular", name_lower="popular")

@app.route("/now_playing/")
@login_required
def now_playing():
    page = int(request.args.get("page"))
    now_playing = findMovies.findNowPlaying(page)
    return render_template("category.html", results=now_playing, page_number=page, pages=list(range(1, 11)), name="Now playing", name_lower="now_playing")

@app.route("/top_rated/")
@login_required
def top_rated():
    page = int(request.args.get("page"))
    top_rated = findMovies.findTopRated(page)
    return render_template("category.html", results=top_rated, page_number=page, pages=list(range(1, 11)), name="Top rated", name_lower="top_rated")

@app.route("/upcoming/")
@login_required
def upcoming():
    page = int(request.args.get("page"))
    upcoming = findMovies.findUpcoming(page)
    return render_template("category.html", results=upcoming, page_number=page, pages=list(range(1, 11)), name="Upcoming", name_lower="upcoming")

@app.route("/change_movie_list_status", methods=["POST"])
def change():
    note = json.loads(request.data)
    list_id = note["list_id"]
    movie_id = note["movie_id"]
    detail = findMovies.getMovieDetails(str(movie_id))
    check = db.execute("SELECT * FROM contains WHERE list_id=? and movie_id = ?", list_id, movie_id)
    if len(check) == 1:
        db.execute("DELETE FROM contains WHERE list_id = ? and movie_id = ?", list_id, movie_id)
    else:
        if len(db.execute("SELECT * FROM movies WHERE id = ?", movie_id)) == 0:
            db.execute("INSERT INTO movies (id, movie_name, poster) VALUES (?, ?, ?)", movie_id, detail["title"], detail["poster_path"])
        db.execute("INSERT INTO contains (list_id, movie_id) VALUES (?, ?)", list_id, movie_id)
    return jsonify({})

def getMovieinList(list_id):
    movies = [i["movie_id"] for i in db.execute("SELECT * FROM contains WHERE list_id = ?", list_id)]
    return movies

