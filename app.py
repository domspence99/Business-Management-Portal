import os   # Includes os environment variables

from cs50 import SQL    # Includes db.execute for SQL databases (Check if correct execution )
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, InputRequired, Length, EqualTo, ValidationError

from helpers import login_required

# Instanciates flask application
app = Flask(__name__)
Bootstrap(app)

# Ensures templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = "qQhh4e2Sd8a1ssDdHvx" # Secret key for form submission
Session(app)

# Configure local database using cs50 sql command
db = SQL("sqlite:///jobs.db")

# Ensures responses aren't cached
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET","POST"])
@login_required
def index():
    # Retrieve jobs to be displayed on homepage
    jobs = db.execute("SELECT * FROM jobs")
    # If posted
    if request.method == "POST":
        # If edit button pressed
        if request.form.get("edit"):
            print(request.form.get("edit"))
            print("delelted")
            return redirect("/")
        # If delete button pressed delete job from database
        if request.form.get("delete"):
            delete_row_id = request.form.get("delete")
            delete_row_from_db(delete_row_id)
            return redirect("/")
        # If view button is pressed
        if request.form.get("view"):
            view_row_id =request.form.get("view")
            return redirect(url_for("view",job_id=view_row_id))  # Passes job id number to view route
    # If refreshed
    if request.method == "GET":

        return render_template("index.html",jobs=jobs)


@app.route("/view/<job_id>",methods=["GET","POST"])  # Row ID passed through to route
@login_required
def view(job_id):
    job_info = get_job_info(job_id)

    if request.method == "POST":
        print("form posted")
        if request.form.get("save"):
            # If form is edited and saved, update the database values with new values
            edit_job = {"job_number":request.form.get("job_number"),"date":request.form.get("date"),
            "customer":request.form.get("customer"), "address":request.form.get("address"), "description":request.form.get("description"),
            "status":request.form.get("status"),"person":request.form.get("person"),
            "visit":request.form.get("visit")}

            # Update database with those new variables at the same row ID
            db.execute("UPDATE jobs SET (date, job_number, shop, address, description, status, person, planned_visit) = (?,?,?,?,?,?,?,?) WHERE id = (?);",
                   edit_job["date"], edit_job["job_number"], edit_job["customer"], edit_job["address"], edit_job["description"], edit_job["status"],
                   edit_job["person"], edit_job["visit"], job_id)
        return redirect("/")

    if request.method == "GET":
        return render_template("view.html",job_id=job_id, job_info=job_info)


@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    add_job = {"job_number":"", "date":"", "customer":"", "address":"", "description":"","status":"","person":"","visit":""}  # Initialising empty job array whenever page is reloaded
    if request.method == "POST":
        # 1. Add to database -> Update on index
        # Obtaining user input from form & adding to dictionary
        add_job["job_number"] = request.form.get("job_number")
        add_job["date"] = request.form.get("date")
        add_job["customer"] = request.form.get("customer")
        add_job["address"] = request.form.get("address")
        add_job["description"] = request.form.get("description")
        add_job["status"] = request.form.get("status")
        add_job["person"] = request.form.get("person")
        add_job["visit"] = request.form.get("visit")
        print(add_job)

        # Insert user input into database
        db.execute("INSERT INTO jobs (date, job_number, shop, address, description, status, person, planned_visit) VALUES (?,?,?,?,?,?,?,?);",
                   add_job["date"], add_job["job_number"], add_job["customer"], add_job["address"], add_job["description"], add_job["status"],
                   add_job["person"], add_job["visit"])
        flash(f"Job {add_job['job_number']} added to system")
        return render_template("add.html")

    if request.method == "GET":
        return render_template("add.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    form = RegistrationForm()  # Initialising form
    if request.method == "POST":
        # If form submitted successfully add username & passwords to database
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?,?);", username, password_hash)  # Insert user credentials into database
            return render_template("registered.html"), {"Refresh": "5; url=/login"}  # Show success message then redirect to login
        return render_template("register.html", form=form)  # If form submission unsuccessful, stay on register page

    if request.method == "GET":
        return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()  # Instantiate log in form
    if request.method == "POST":
        if form.validate_on_submit():  # Retreive form data on submission
            username = form.username.data
            password = form.password.data

            log_in_validation = check_credentials(username,password)  # Check if log in is valid
            if log_in_validation == False:  # If log in unsuccessful, render log in and error message
                return render_template("login.html", form=form, log_in_validation=log_in_validation)
            else:
                flash("Successfully logged in")
                return redirect("/")  # Successful login


        return render_template("login.html", form=form)
    if request.method == "GET":
        return render_template("login.html",form=form)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("You have been logged out")
    return redirect("/")

# Create a Form Class
class RegistrationForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired("Username must be between 4 and 15 characters"), Length(min=4, max=15)])  #Ensures username validation
    # Checks if username is already in database
    def validate_username(self, username):
        print(username.data)
        username_rows = db.execute("SELECT * FROM users WHERE username = (?);", username.data)
        if len(username_rows) != 0:
            print("error")
            raise ValidationError("Username already taken")

    # Checks password lengths & ensures they are matching
    password = PasswordField("Password", validators=[InputRequired("Password must be between 8 and 50 characters"), Length(min=8, max=50)])
    password_confirmation = PasswordField("Password Confirmation", validators=[InputRequired("Passwords must match"), Length(min=8,max=50), EqualTo("password",message="Passwords must match")])  # Ensures passwords don't match

class LoginForm(FlaskForm):
    # Ensures valid username and password input
    username = StringField("Username",validators=[InputRequired("Username must be between 4 and 15 characters"), Length(min=4, max=15)])  #Ensures username validation
    password = PasswordField("Password", validators=[InputRequired("Password must be between 8 and 50 characters"), Length(min=8, max=50)])

def check_credentials(username,password):
    row = db.execute("SELECT * FROM users WHERE username = (?);",username)
    print(row)
    if len(row)!=1:
        print(len(row))
        return False
    elif not check_password_hash(row[0]["hash"],password):
        return False
    else:
        session["user_id"] = row[0]["id"]
        return True
# Function to delete a row from the database
def delete_row_from_db(id):
    db.execute("DELETE FROM jobs WHERE id = (?);", id)
    return True
# Function to pass row view across pages
def obtain_view_row_id(id):
    return id

def get_job_info(id):
    job_info = db.execute("SELECT * FROM jobs WHERE id = (?);",id)
    if len(job_info) != 1:
        return None
    else:
        return job_info[0]
