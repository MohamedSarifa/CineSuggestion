import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from dotenv import load_dotenv

from database import db
from models import User, Watchlist
from movies import movies
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

# ================= APP CONFIG =================

load_dotenv()

app = Flask(__name__)

app.secret_key = "cinesuggestion_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ================= HOME =================

@app.route("/")
def home():

    return render_template(
        "index.html",
        movies=movies,
        username=session.get("username")
    )


# ================= REGISTER =================

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/save_user", methods=["POST"])
def save_user():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()

    if existing_user:
        return "Username or Email already exists."

    new_user = User(
    username=username,
    email=email,
    password=generate_password_hash(password)
)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login"))


# ================= LOGIN =================

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/check_login", methods=["POST"])
def check_login():

username = request.form["username"]
password = request.form["password"]

user = User.query.filter_by(
    username=username
).first()

if user and check_password_hash(
        user.password,
        password):

    session["username"] = username

    return redirect(url_for("home"))

return "Invalid Username or Password"



# ================= LOGOUT =================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# ================= SEARCH =================

@app.route("/search", methods=["POST"])
def search():

    movie = request.form["movie"].title()

    if movie in movies:
        recommendations = movies[movie]["recommendations"]
    else:
        recommendations = []

    return render_template(
        "result.html",
        movie=movie,
        recommendations=recommendations,
        movies=movies,
        username=session.get("username")
    )


# ================= DETAILS =================

@app.route("/details/<name>")
def details(name):

    if name not in movies:
        return "Movie Not Found"

    return render_template(
        "details.html",
        name=name,
        movie=movies[name],
        username=session.get("username")
    )


# ================= ADD WATCHLIST =================

@app.route("/add/<name>")
def add_to_watchlist(name):

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    movie = Watchlist.query.filter_by(
        username=username,
        movie_name=name
    ).first()

    if not movie:

        new_movie = Watchlist(
            username=username,
            movie_name=name
        )

        db.session.add(new_movie)
        db.session.commit()

    return redirect(url_for("my_watchlist"))


# ================= WATCHLIST =================

@app.route("/watchlist")
def my_watchlist():

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    rows = Watchlist.query.filter_by(
        username=username
    ).all()

    watchlist = [
        row.movie_name
        for row in rows
    ]

    return render_template(
        "watchlist.html",
        watchlist=watchlist,
        movies=movies,
        username=username
    )


# ================= REMOVE MOVIE =================

@app.route("/remove/<name>")
def remove_movie(name):

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    movie = Watchlist.query.filter_by(
        username=username,
        movie_name=name
    ).first()

    if movie:

        db.session.delete(movie)

        db.session.commit()

    return redirect(url_for("my_watchlist"))

@app.route("/dashboard")
def dashboard():


if "username" not in session:
    return redirect(url_for("login"))

username = session["username"]

total = Watchlist.query.filter_by(
    username=username
).count()

return render_template(
    "dashboard.html",
    username=username,
    total=total
)


# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)