# ---- View Routes (Page Rendering) ----



@app.route("/insights", methods=["GET", "POST"])
@login_required
def insights():
    return render_template('insights.html')



# ---- API Flask Routes (Functions that Handle Functionality/Database Interaction) ----



# Allows a user to delete a timer category
@app.route("/delete_timer", methods=["POST"])
@login_required
def delete_timer():
    if request.method == "POST":

        data = request.get_json()
        timer_name = data.get('timer_name')
    rows = db.execute("SELECT id FROM timers WHERE timer_name = ?", timer_name)

    session["timer_id"] = rows[0]["id"]

    db.execute("DELETE FROM timers_log WHERE timers_id = ?", session["timer_id"])
    db.execute("DELETE FROM timers WHERE id = ?", session["timer_id"])

    response = {'status': 'success', 'received': data}
    return jsonify(response), 200




@app.route("/add_timers_time_logged", methods=["POST"])

# Enables a user to dinamically change the timers name on index page
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




@app.route("/timers", methods=["GET", "POST"])
@login_required
def timers():

    # --- This gets all the timers names ---
    rows_timer_name_id = db.execute(
        "SELECT timer_name, id FROM timers WHERE user_id = ?", session["user_id"])
    timers = []
    for row in rows_timer_name_id:
        timers.append({
            "names": row['timer_name']
        })
    print(timers)

    # --- This gets all the timers ids ---
    user_timer_ids = db.execute(
        "SELECT id FROM timers WHERE user_id = ?", session["user_id"])
    timer_ids = []

    for row in user_timer_ids:
        timer_ids.append(
            {"timer_id": row['id']}
        )
    print(timer_ids)

    # --- This sums up every time logged for each timer using the timers id list
    for row in timer_ids:
        print(db.execute("SELECT SUM(time_logged) FROM timers_log WHERE user_id = ? AND timers_id = ?",
              session["user_id"], row['timer_id']))

    # TODO I need to figure out how too append all this data into one list
    # timer_id, timer_name, and sum_time_logged into one list

    return render_template('timers.html', timers=timers)
    #   THE LIST OF TIMERS                                                  CHECKMARK!
    # 1. Get all timer id's associated with the same user_id                CHECKMARK!

    #   USE THE LIST OF TIMERS TO FIND ALL TIME LOGGED FOR EACH
    # 2. loop through each timer id                                         CHECKMARK!!
    #   search the database for all time_logged belonging to that specific timer id "SUM(time_logged) FROM timers_log WHERE user_id = ? AND timers_id = ?", session[user_id], current timer_id)       CHECKMARK!!!

    # 3. insert each timers name (found via id) and all the time logged into the llist as one dictionary entry per each



    # this is just simple form mechanics now

    # Get form data (maybe we have to split it up, form data from one and form data from the other im not sure how i can interact with a form i submit with multiple peices of data )

    # If current selections name is selected with radio button delete everything about that timer (maybe issuse a warning modal before it goes through)

    # If name feild has name in it that isnt over 15 characters long (or whatever amount you want) and if the feild has anything in it at all then change the name of that category of timer

    # TODO watch video on forms to refresh yourself.
