from flask import Flask, render_template
from flask import request, redirect
from flask import url_for, session

from database import cursor, conn
from movies import movies

app = Flask(__name__)
app.secret_key = "cinesuggestion_secret"


# ================= HOME =================

@app.route("/")
def home():

    username = session.get("username")

    return render_template(
        "index.html",
        movies=movies,
        username=username
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

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password)
            VALUES (?, ?, ?)
            """,
            (username, email, password)
        )

        conn.commit()

        return redirect(url_for("login"))

    except:
        return "Username or Email already exists."


# ================= LOGIN =================

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/check_login", methods=["POST"])
def check_login():

    username = request.form["username"]
    password = request.form["password"]

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (username, password)
    )

    user = cursor.fetchone()

    if user:
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


# ================= ADD TO WATCHLIST =================

@app.route("/add/<name>")
def add_to_watchlist(name):

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    cursor.execute(
        """
        SELECT *
        FROM watchlist
        WHERE username = ?
        AND movie_name = ?
        """,
        (username, name)
    )

    movie = cursor.fetchone()

    if not movie:

        cursor.execute(
            """
            INSERT INTO watchlist
            (username, movie_name)
            VALUES (?, ?)
            """,
            (username, name)
        )

        conn.commit()

    return redirect(url_for("my_watchlist"))


# ================= WATCHLIST =================

@app.route("/watchlist")
def my_watchlist():

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    cursor.execute(
        """
        SELECT movie_name
        FROM watchlist
        WHERE username = ?
        """,
        (username,)
    )

    rows = cursor.fetchall()

    watchlist = []

    for row in rows:
        watchlist.append(row[0])

    return render_template(
        "watchlist.html",
        watchlist=watchlist,
        movies=movies,
        username=username
    )


# ================= REMOVE FROM WATCHLIST =================

@app.route("/remove/<name>")
def remove_movie(name):

    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    cursor.execute(
        """
        DELETE FROM watchlist
        WHERE username = ?
        AND movie_name = ?
        """,
        (username, name)
    )

    conn.commit()

    return redirect(url_for("my_watchlist"))


# ================= RUN APP =================

if __name__ == "__main__":
    app.run(debug=True)
    