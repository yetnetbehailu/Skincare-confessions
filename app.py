import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["Mongo_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['SECRET_KEY'] = 'SECRET_KEY'
mongo = PyMongo(app)


"""
#   Home Route
-------------------

"""


@app.route('/home')
def home():
    return render_template('home.html')


"""
#   Add Reviews Route
-------------------

"""


@app.route("/")
@app.route("/add_reviews")
def add_reviews():
    reviews = mongo.db.reviews.find()
    return render_template("add_reviews.html", reviews=reviews)


"""
#   My Reviews Route
-------------------

"""


@app.route('/my_reviews/<username>', methods=['GET', 'POST'])
def my_reviews(username):
    # Grab sessions username from db
    username = mongo.db.users.find_one({'username':
                                        session['user'].lower()})['username']
    return render_template('my_reviews.html', username=username)


"""
# Register Route
-------------------
# When registering for an account, if username input does not already exists
# in database, and password fields do match then a new user is created.
# To make password extra secure it's hashed using werkzeug.security.
# Once registration is valid user is automatically logged in and re-directed to
# home page.
"""


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username already exist in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form["username"].lower()})
        if existing_user:
            flash('Sorry, this username has been taken')
            return redirect(url_for("register"))
        else:
            new_user = {
                "username": request.form["username"].lower(),
                "password": generate_password_hash(request.form["password"])
            }
            mongo.db.users.insert_one(new_user)

            # Put the new user into 'session' cookie
            session["user"] = request.form["username"]
            flash('Account successfully created for'
                  f' {form.username.data}\u2713', 'success')
            return redirect(url_for('home'))
    return render_template("register.html", title='Register', form=form)


"""
# Login Route
 ---------------
# when logging in to account if user exists in database,
# is re-directed to home page else login page displayed.
# The input password has to match the hashed password saved in database
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form["username"].lower()})
        if existing_user:
            # Verify hashed password matches user input
            if check_password_hash(existing_user["password"],
                                   request.form["password"]):
                # If password match add user to session cookie
                session["user"] = request.form["username"]
                flash('Welcome back'f' {form.username.data}\u0021', 'success')
                return redirect(url_for('home'))
            else:
                # Password not a match
                flash('Username or password is incorrect. Please try again ',
                      'danger')
                return redirect(url_for("login"))
        else:
            # username doesn't exist
            flash('Username or password is incorrect. Please try again ',
                  'danger')
            return redirect(url_for("login"))
    return render_template("login.html", title='Login', form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # Change to false before final deployment, delete msg
