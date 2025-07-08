from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        flash("You are already logged in!", "info")
        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session["user"] = user.email
            flash("Login successful!", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid email or password", "danger")

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])




@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user" in session:
        flash("You are already logged in!", "info")
        return redirect("/dashboard")
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already exists. Please log in.", "warning")
            return redirect("/login")

        # Create and save new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session["user"] = email
        flash("Signup successful!", "success")
        return redirect("/dashboard")

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
