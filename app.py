from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import Config
from models import db, User, Task

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

    user = User.query.filter_by(email=session["user"]).first()
    
    if not user:
        
        session.clear()
        flash("Session expired. Please log in again.", "warning")
        return redirect("/login")

    tasks = user.tasks
    
    
    
    return render_template("dashboard.html", user=user.email, tasks=tasks)

@app.route("/add-task", methods=["POST"])
def add_task():
    if "user" not in session:
        flash("You must be logged in to add tasks.", "danger")
        return redirect("/login")

    title = request.form["title"]
    description = request.form.get("description")  # optional field

    user = User.query.filter_by(email=session["user"]).first()

    new_task = Task(title=title, description=description, user=user)

    db.session.add(new_task)
    db.session.commit()

    flash("Task created successfully!", "success")
    return redirect("/dashboard")

@app.route("/delete-task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user" not in session:
        flash("You must be logged in to delete tasks.", "danger")
        return redirect("/login")

    user = User.query.filter_by(email=session["user"]).first()
    task = Task.query.get(task_id)

    # ✅ Allow deletion only if task belongs to current user
    if task and task.user_id == user.id:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully!", "success")
    else:
        flash("Task not found or permission denied.", "danger")

    return redirect("/dashboard")
    
@app.route("/mark-done/<int:task_id>", methods=["POST"])
def mark_done(task_id):
    if "user" not in session:
        flash("Please log in first.", "warning")
        return redirect("/login")

    task = Task.query.get(task_id)

    if task:
        task.is_completed = True
        db.session.commit()
        flash("✅ Task marked as completed!", "success")
    else:
        flash("Task not found.", "danger")

    return redirect("/dashboard")


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
