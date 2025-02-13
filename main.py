from flask import Flask, render_template, request, session, redirect, url_for
import db

app = Flask(__name__)
app.secret_key = "sevenfoursevenseven"

@app.route("/")
def Home():
    reviews = db.GetAllReviews()
    return render_template("index.html", reviews=reviews)

@app.route("/login", methods=["GET", "POST"])
def Login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = db.CheckLogin(username, password)
        if user:
            session['id'] = user['id']
            session['username'] = user['username']
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if db.RegisterUser(username, password):
            return redirect("/")
    return render_template("register.html")

@app.route("/add", methods=["GET","POST"])
def Add():
    if session.get('username') is None:
        return redirect("/login")
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        game = request.form['game']
        score = request.form['score']
        review = request.form['review']
        db.AddReview(user_id, date, game, score, review)
    return render_template("add.html")

@app.route("/update/<int:review_id>", methods=["GET", "POST"])
def Update(review_id):
    if session.get('username') is None:
        return redirect("/login")
    review = db.GetReviewById(review_id)
    if review is None:
        return redirect("/")
    if request.method == "POST":
        score = request.form['score']
        review_text = request.form['review']
        db.UpdateReview(review_id, score, review_text)
        return redirect("/")
    return render_template("update.html", review=review)

@app.route("/reset")
def Reset():
    db.ResetDatabase()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)