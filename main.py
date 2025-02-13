from flask import Flask, render_template, request, session, redirect, url_for
import db

app = Flask(__name__)
app.secret_key = "sevenfoursevenseven"

@app.route("/")
def Home():
    guessData = db.GetAllGuesses()
    return render_template("index.html", guesses=guessData)

@app.route("/login", methods=["GET", "POST"])
def Login():
    # They sent us data, get the username and password
    # then check if their details are correct.
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Did they provide good details
        user = db.CheckLogin(username, password)
        if user:
            # Yes! Save their username and id then
            session['id'] = user['id']
            session['username'] = user['username']

            # Send them back to the homepage
            return redirect("/")

    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():
    # If they click the submit button, let's register
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # Try and add them to the DB
        if db.RegisterUser(username, password):
            # Success! Let's go to the homepage
            return redirect("/")
        
    return render_template("register.html")

@app.route("/add", methods=["GET","POST"])
def Add():
    # Check if they are logged in first
    if session.get('username') == None:
        return redirect("/")

    # Did they click submit?
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        game = request.form['game']
        score = request.form['score']
        review = request.form['review']

        # Send the data to add our new guess to the db
        db.AddGuess(user_id, date, game, score, review)

    return render_template("add.html")

@app.route("/update/<int:guess_id>", methods=["GET", "POST"])
def Update(guess_id):
    # Check if the user is logged in first
    if session.get('username') is None:
        return redirect("/login")

    # Fetch the existing guess from the database
    guess = db.GetGuessById(guess_id)  # Get guess data by ID

    if guess is None:
        return redirect("/")  # If the guess doesn't exist, redirect to homepage

    if request.method == "POST":
        # Get updated data from the form
        score = request.form['score']
        review = request.form['review']

        # Update the guess in the database
        db.UpdateGuess(guess_id, score, review)
        return redirect("/")  # Redirect to the homepage after update

    # Render the update page with the current guess data
    return render_template("update.html", guess=guess)

if __name__ == "__main__":
    app.run(debug=True, port=5000)