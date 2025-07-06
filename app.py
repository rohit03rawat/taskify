from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import db

users = {}  # just for testing — will store email-password pairs

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
       
        if email in users and users[email] == password:
            session["user"] = email
            return redirect(url_for("dashboard"))

        else:
            return "Invalid credentials. Try again."

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return f"Welcome {session['user']}! This is your dashboard."


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email in users:
            return "User already exists. Please login."
        
        # Save user
        users[email] = password
        return redirect(url_for("login"))

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
