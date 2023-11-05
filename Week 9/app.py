import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    total=0;
    wallets = db.execute("SELECT * FROM wallet WHERE user_id= ?", session["user_id"])
    for row in wallets:
        row['price'] = lookup(row['symbol'].upper())['price']
        row['price'] = usd(row['price'])
        total = total + float(row["value"])
        row['value'] = usd(row['value'])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total_final = cash[0]["cash"] + total
    return render_template("index.html", portfolios=wallets, total=usd(total_final), cash=usd(cash[0]['cash']))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not lookup(symbol):
            return apology("Invalid ticket", 400)
        try:
            aux = int(shares)
        except ValueError:
             return apology("must introduce a number", 400)
        if int(shares) < 1:
            return apology("must introduce a positive number", 400)
        if len(lookup(symbol)) < 1 or not symbol:
            return apology("Invalid symbol", 400)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        price = lookup(symbol)['price']
        if cash[0]['cash'] > (float(price)*int(shares)):

            """REGISTER TRANSACTION"""

            cash[0]['cash']= cash[0]['cash'] - (float(price)*int(shares))
            db.execute ("INSERT INTO transactions (user_id, symbol, price, quantity, date, type) VALUES (?,?,?,?, DATE('now'), 'BUY')", session["user_id"], symbol, price, shares)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash[0]['cash'], session["user_id"])

            """ UPDATE PORTFOLIO """

            quantity= db.execute("SELECT quantity FROM wallet WHERE user_id = ? and symbol = ?", session["user_id"], symbol)
            if len(quantity)==0:
                db.execute ("INSERT INTO wallet (user_id, symbol, value, quantity) VALUES (?,?,?,?)", session["user_id"], symbol, (float(price)*int(shares)), int(shares))
            else:
                new_quantity = quantity[0]['quantity'] + int(shares)
                value = new_quantity * float(price)
                db.execute("UPDATE wallet SET quantity = ?, value = ? WHERE symbol = ? and user_id = ?", new_quantity,  value, symbol, session["user_id"])
        else:
            return apology("Not enough money", 403)
        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT * FROM transactions WHERE user_id= ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        quotes = lookup(request.form.get("symbol"))
        if not quotes:
             return apology("Invalid ticket", 400)
        return render_template("quoted.html", quotes=quotes['price'])

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

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    list_companies=[]
    if request.method == "GET":
        companies = db.execute("SELECT symbol FROM wallet")
        for row in companies:
            list_companies.append(row['symbol'])
        return render_template("sell.html", options=list(set(list_companies)))
    else:
        if int(request.form.get("shares")) < 1:
            return apology("must introduce a positive number", 400)
        if not request.form.get("symbol"):
            return apology("must introduce a valid symbol", 400)
        wallet_symbol = db.execute("SELECT quantity FROM wallet WHERE symbol = ?", request.form.get("symbol"))

        if len(wallet_symbol) == 0:
            return apology("You don't have any stocks yet", 400)

        elif wallet_symbol[0]['quantity'] >= int(request.form.get("shares")):
            new_quantity = wallet_symbol[0]['quantity'] - int(request.form.get("shares"))
            value = new_quantity * float(lookup(request.form.get("symbol"))['price'])
            db.execute("UPDATE wallet SET quantity = ?, value = ? WHERE symbol = ? and user_id= ?", new_quantity,  value, request.form.get("symbol"), session["user_id"])
            db.execute ("INSERT INTO transactions (user_id, symbol, price, quantity, date, type) VALUES (?,?,?,?, DATE('now'), 'SELL')", session["user_id"], request.form.get("symbol"), float(lookup(request.form.get("symbol"))['price']), int(request.form.get("shares")))
            cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
            first_row=cash[0]
            first_row['cash'] = first_row['cash'] + (int(request.form.get("shares"))*float(lookup(request.form.get("symbol"))['price']))
            db.execute("UPDATE users SET cash = ? WHERE id = ?",  cash[0]['cash'], session["user_id"])
        else:
            return apology("You don't have enough of that stock", 400)
        return redirect("/")

