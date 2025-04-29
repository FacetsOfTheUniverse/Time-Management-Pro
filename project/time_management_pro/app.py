from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology


# Configure Flask Application
app = Flask(__name__)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///timer.db")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Prevent HTTP from caching so data is most up to date
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# ---- View Routes (Page Rendering) ----

# Home Page
@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # --- Pass a list of dictionaries for use when displaying timer information
    rows_timer_names = db.execute(
        "SELECT id, timer_name FROM timers Where user_id = ?", session["user_id"])

    timers = []
    for row in rows_timer_names:
        timers.append({
            "id": row["id"],
            "names": row['timer_name']
        })

    return render_template('index.html', timers=timers)

# Timers Page
@app.route("/timers", methods=["GET", "POST"])
@login_required
def timers():

    # --- Preparing a list of dictionaries ---
    # (Grok AI helped me here mostly with getting the 00:00:00 display to work correctly)
    rows_timer_name_id = db.execute(
        "SELECT timer_name, id FROM timers WHERE user_id = ?", session["user_id"])
    timers = []
    for row in rows_timer_name_id:
        timers.append({
            "id": row["id"],
            "name": row["timer_name"],
            "total_time_logged": 0
        })

    for timer in timers:
        sum = (db.execute("SELECT SUM(time_logged) AS total FROM timers_log WHERE user_id = ? AND timers_id = ?",
                          session["user_id"], timer["id"]))
        total_time = sum[0]["total"] if sum[0]["total"] is not None else 0
        total_seconds = total_time // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        total_time = f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"
        timer["total_time_logged"] = total_time

    return render_template('timers.html', timers=timers)


# ---- API Flask Routes (Functions that Handle Functionality/Database Interaction) ----


# Allows a user to create timer categorys
@app.route("/add_new_timer", methods=["POST"])
@login_required
def add_new_timer():

    if request.method == "POST":

        new_timer = request.form.get("new_timer")
        if not new_timer:
            return apology("missing timer name", 400)

        if new_timer is None:
            return apology("invalid symbol", 400)

        db.execute("INSERT INTO timers (user_id, timer_name) VALUES(?, ?)",
                   session["user_id"], new_timer)

        flash("New Timer Created!")
        return redirect("/")



# Informs the server which timer is currently being operated, ensuring proper saving functionality
@app.route("/update_timer_name", methods=["POST"])
@login_required
def update_timer_name():
    if request.method == "POST":

        data = request.get_json()
        timer_name = data.get('timer_name')
    rows = db.execute("SELECT id FROM timers WHERE timer_name = ?", timer_name)

    session["timer_id"] = rows[0]["id"]

    response = {'status': 'success', 'received': data}
    return jsonify(response), 200



# Enables a user to edit the name of their timer or delete it
@app.route('/edit_timer', methods=["GET", "POST"])
@login_required
def edit_timer():
    timer_id = request.form.get('timer_id')  # The timer’s DB id
    action = request.form.get('action')      # 'delete' or None
    rename_value = request.form.get('rename_timer', '').strip()  # New name or empty

    if not timer_id:
        return "Error: No timer ID provided", 400  # Basic error handling

    if action == 'delete':
        # Delete the timer from the database
        db.execute("DELETE FROM timers_log WHERE timers_id = ? AND user_id = ?",
                   timer_id, session["user_id"])
        db.execute("DELETE FROM timers WHERE id = ? AND user_id = ?",
                   timer_id, session["user_id"])
        print(f"Deleted timer with ID: {timer_id}")
        flash("Timer Deleted!")
    elif rename_value:
        # Update the timer’s name in the database
        db.execute("UPDATE timers SET timer_name = ? WHERE id = ? AND user_id = ?",
                   rename_value, timer_id, session["user_id"])
        print(f"Renamed timer {timer_id} to: {rename_value}")

    return redirect("/")  # Redirect to refresh the list
# Originally I had the delete and rename methods seperate but Grok helped me fine tune each and combine them together


# Enables the user to save their timers
@app.route("/save_timer_entry", methods=["POST"])
@login_required
def save_timer_entry():
    try:
        data = request.get_json()
        startTimestamp = data.get('startTimestamp')
        stopTimestamp = data.get('stopTimestamp')
        timeClocked = data.get('timeClocked')
        db.execute("INSERT INTO timers_log (start_timestamp, stop_timestamp, time_logged, user_id, timers_id) VALUES(?, ?, ?, ?, ?)",
                   startTimestamp, stopTimestamp, timeClocked, session["user_id"], session["timer_id"])
        response = {'status': 'success', 'received': data}
        return jsonify(response), 200

    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in save_timer_entry: {e}")
        # Return JSON even on error
        return jsonify({'status': 'error', 'message': str(e)}), 500
        # Save timer data to the correct timer


# ---- Login Routes (Login/Logout/Register Functionality) ----

# These Login Routes are all reused from our finance project from week 9


# Enables the user to login
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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


# Enables the user to logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Enables the user to register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("missing username", 400)

        # Ensure password 1 and 2 was submitted and are the same
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords dont match", 400)

        # Query database for username
        check_username = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        # Ensure username isnt taken
        if check_username:

            return apology("username taken")

        # add hashed password and username to the database
        else:
            hashed_password = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                   request.form.get("username"), hashed_password)

        # Remember which user has logged in
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        # Flash registred!!
        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")
