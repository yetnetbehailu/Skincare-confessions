from flask import flash, render_template, redirect, request, session, url_for
from skincare_confessions import app, mongo
from skincare_confessions.forms import RegisterForm, LoginForm
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

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


@app.route('/my_reviews', methods=['GET', 'POST'])
def my_reviews():
    # Grab sessions username from db
    if 'user' in session:
        username = mongo.db.users.find_one({'username':
                                            session['user'].lower()
                                            })['username']
        return render_template('my_reviews.html', username=username)
    else:
        return redirect(url_for('login'))
    print(my_reviews())


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
                # Link clicked prior to login get URI parameter & re-direct to
                # page on login
                view_next = request.args.get('view')
                return redirect(view_next) if view_next else redirect(url_for
                                                                      ('home'))
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


@app.route('/logout')
def logout():
    # Deletes user session cookie removes logged in state
    session.pop('user')
    return redirect(url_for('login'))
