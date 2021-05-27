from flask import flash, render_template, redirect, request, session, url_for
from skincare_confessions import app, mongo
from skincare_confessions.forms import RegisterForm, LoginForm, AddReviewForm
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from bson.decimal128 import Decimal128

reviews = mongo.db.reviews
categories = mongo.db.categories

"""
#   Home Route
-------------------

"""


@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')


"""
#   Add Reviews Route
-------------------
#
"""


@app.route("/add_reviews", methods=["GET", "POST"])
def add_reviews():
    """ Displays Add review form when user is logged in, preventing guest
        users access.
        Logged in user is able to create a review which when submitted gets
        inserted to reviews collection in database.
        Validation requirements must be meet according to AddReview Flaskform.
        Upon successful submission user is re-directed to their personal
        reviews collection page. If unable to make a successful entry user
        remains on the current page.
     """

    if 'user' in session:
        username = mongo.db.users.find_one({'username':
                                            session['user'].lower()
                                            })['username']
        add_review_form = AddReviewForm()
        category_name = categories.find()
        if add_review_form.validate_on_submit():
            is_vegan = True if request.form.get("is_vegan") else False
            price = Decimal128(str((request.form.get('price'))))
            rating = int(request.form.get('rating'))
            review = {
                'category_name': request.form.get('category_name'),
                'brand_name ': request.form.get('brand_name'),
                'product_review': request.form.get('product_review'),
                'price': (price),
                'is_vegan': (is_vegan),
                'rating': (rating),
                'tags ': request.form.get('tags'),
            }
            reviews.insert_one(review)
            flash('Review successfully added', 'succes')
            return redirect(url_for('my_reviews', review=review,
                            is_vegan=is_vegan, price=price, rating=rating))
        return render_template("add_reviews.html", username=username,
                               category_name=category_name,
                               form=add_review_form)
    return redirect(url_for('login'))


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
            if check_password_hash(
                    existing_user["password"], request.form["password"]):
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


"""
# Logout Route
 ---------------
# When user (clicks)log out is re-directed to login page.
"""


@app.route('/logout')
def logout():
    # Deletes user session cookie removes logged in state
    session.pop('user')
    return redirect(url_for('login'))
