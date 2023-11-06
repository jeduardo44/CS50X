import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from aux import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///goals.db")

months=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November","December"]


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        goals = db.execute("SELECT * FROM goals WHERE user_id = ?", session["user_id"])
        for row in goals:
            row['remaining'] = row['value'] - row['invested']
            if row['remaining'] < 0:
                row['remaining'] = 0
        return render_template("index.html", goals=goals)

@app.route("/reinforcement", methods=["GET", "POST"])
@login_required
def reinforcement():
    if request.method == "GET":
        reinforcements = db.execute("SELECT * FROM reinforcements WHERE user_id = ?", session["user_id"])
        for row in reinforcements:
            goal=db.execute("SELECT description FROM goals WHERE id= ?", row["goal_id"])
            row["goal"] = goal[0]["description"]
        return render_template("reinforcements.html", reinforcements=reinforcements, months=months)
    elif request.method == "POST":
        month = request.form.get("month")
        if month == "All":
            reinforcements = db.execute("SELECT * FROM reinforcements WHERE user_id = ?", session["user_id"])
            for row in reinforcements:
                goal=db.execute("SELECT description FROM goals WHERE id= ?", row["goal_id"])
                row["goal"] = goal[0]["description"]
            return render_template("reinforcements.html", reinforcements=reinforcements, months=months)
        if not month or month not in months:
            return apology("Invalid month", 400)
        reinforcements = db.execute("SELECT * FROM reinforcements WHERE user_id = ? and month = ?", session["user_id"], month)
        for row in reinforcements:
            goal=db.execute("SELECT description FROM goals WHERE id= ?", row["goal_id"])
            row["goal"] = goal[0]["description"]
        return render_template("reinforcements.html", reinforcements=reinforcements, months=months)


@app.route("/new_goal", methods=["GET","POST"])
@login_required
def goal():
    if request.method == "POST":
        goal = request.form.get("goal")
        value= request.form.get("value")
        type = request.form.get("type")
        if not goal or not value or not type:
            return apology("Error in the form", 400)
        db.execute("INSERT INTO goals (user_id, description, value, type, status, invested) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], goal, float(value), type, "INCOMPLETED", 0)
        return redirect("/")
    else:
        return render_template("new_goal.html")

@app.route("/new_reinforcement", methods=["GET","POST"])
@login_required
def new_reinforcement():
    if request.method == "POST":
        goal = request.form.get("goal")
        value= request.form.get("value")
        month = request.form.get("month")
        if not goal or not value or not month:
            return apology("Error in the form", 400)
        goal_type_id=db.execute("SELECT id, type, invested, value FROM goals WHERE description = ?", goal)
        try:
            value = float(value)
        except ValueError:
             return apology("must introduce a number", 400)
        db.execute("INSERT INTO reinforcements (user_id, goal_id, type, value, month) VALUES (?, ?, ?, ?, ?)", session["user_id"], int(goal_type_id[0]['id']), goal_type_id[0]['type'], value, month)
        db.execute("UPDATE goals SET invested = ? WHERE id =? and user_id = ?", float(goal_type_id[0]['invested'])+float(value), goal_type_id[0]['id'], session["user_id"])
        if (float(goal_type_id[0]['invested'])+float(value)) >= float(goal_type_id[0]['value']):
            db.execute("UPDATE goals SET status = ? WHERE id =? and user_id = ?", "COMPLETED", goal_type_id[0]['id'], session["user_id"])
        return redirect("/")
    else:
        goals= db.execute("SELECT description FROM goals")
        return render_template("new_reinforcement.html", months=months, goals=goals)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("must provide password", 400)
        else:
            usernames = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))
            if usernames:
                return apology("This username already exists", 400)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))
            return redirect("/")
