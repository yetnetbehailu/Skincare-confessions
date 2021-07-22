from flask import (
    flash, render_template, redirect, request, session, url_for, Response)
from skincare_confessions import app, mongo
from skincare_confessions.forms import (
    RegisterForm, LoginForm, AddReviewForm, EmailForm)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from bson.decimal128 import Decimal128
import math
from flask_pymongo import pymongo
from datetime import datetime
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api


cloudinary.config(
    cloud_name=os.environ.get('cloud_name'),
    api_key=os.environ.get('api_key'),
    api_secret=os.environ.get('api_secret')
)

reviews = mongo.db.reviews
categories = mongo.db.categories
users = mongo.db.users
subscribes = mongo.db.subscriptions

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
        inserted to reviews collection in database. Users uploaded image files
        are uploaded & stored in Cloudinary.
        Validation requirements must be meet according to AddReview Flaskform.
        Upon successful submission user is re-directed to their personal
        reviews collection page. If unable to make a successful entry user
        remains on the current page.
     """

    if 'user' in session:
        username = users.find_one({'username':
                                   session['user'].lower()
                                   })['username']
        add_review_form = AddReviewForm()
        category_name = categories.find()
        if add_review_form.validate_on_submit():
            if add_review_form.upload_img.data:
                upload_img = request.files.get('upload_img')
                cloud_upload = cloudinary.uploader.upload(
                    upload_img, width=580, radius=20, height=580)
                uploaded_image = cloud_upload.get('secure_url')
            else:
                uploaded_image = request.form.get('upload_img')
            is_vegan = True if request.form.get("is_vegan") else False
            price = float(str((request.form.get('price'))))
            rating = int(request.form.get('rating'))
            brand_name = str(request.form.get('brand_name'))
            tags = request.form.get('tags').split(",")
            review = {
                'category_name': request.form.get('category_name'),
                'brand_name': brand_name,
                'product_review': request.form.get('product_review'),
                'price': price,
                'is_vegan': is_vegan,
                'rating': rating,
                'tags': tags,
                'added_by': session["user"].lower(),
                'upload_img': uploaded_image,
                'created_on': datetime.today().strftime("%d %b, %Y"),
                'faved_by': []
            }
            reviews.insert_one(review)
            flash('Review successfully added', 'succes')
            return redirect(url_for('my_reviews', review=review))
        return render_template("add_reviews.html", username=username,
                               category_name=category_name,
                               form=add_review_form)
    return redirect(url_for('login'))


"""
#   My Reviews Route
-------------------
Displays users added reviews on personal page for personal view , 12 review
cards per page limit.Total amount of personal published reviews is counted for,
arranged latest to oldest post.
"""


@app.route('/my_reviews')
def my_reviews():
    # Grab sessions username from db
    if 'user' in session:
        username = users.find_one({'username':
                                   session['user'].lower()
                                   })['username']
        user_id = users.find_one({'username': session['user'].lower()})['_id']
        add_review_form = AddReviewForm()
        # Finds & counts user personal review entries
        my_total_reviews = reviews.find({
            "added_by": session["user"].lower()}).count()
        card_per_page = 12
        current_page = int(request.args.get('current_page', 1))
        pages = range(1, int(math.ceil(my_total_reviews / card_per_page)) + 1)
        # Sorts latest entry first skipping the given number of documents in
        # the query.
        author = reviews.find({
            "added_by": session["user"].lower()}).sort(
                '_id', pymongo.DESCENDING).skip(
                (current_page - 1)*card_per_page).limit(card_per_page)
        return render_template(
            'my_reviews.html', username=username, author=author,
            title='My Reviews', my_total_reviews=my_total_reviews,
            pages=pages, current_page=current_page,
            form=add_review_form, user_id=user_id)
    return redirect(url_for('login'))


"""
#   All Reviews listing Route
-------------------

"""


@app.route('/browse_reviews')
def browse_reviews():
    """ Displays added reviews for public view, 12 review cards per page limit.
    Total amount of published reviews is counted for, arranged latest to oldest
    post
    """
    total = reviews.count()
    card_per_page = 12
    current_page = int(request.args.get('current_page', 1))
    pages = range(1, int(math.ceil(total / card_per_page)) + 1)
    # Sorts latest entry first skipping the given number of documents in the
    # query.
    entries = reviews.find().sort('_id', pymongo.DESCENDING).skip(
        (current_page - 1)*card_per_page).limit(card_per_page)
    add_review_form = AddReviewForm()
    if 'user' in session:
        user_id = users.find_one({'username': session['user'].lower()})['_id']
        return render_template(
            'browse_reviews.html', title='All Reviews', entries=entries,
            total=total, pages=pages, current_page=current_page,
            form=add_review_form, user_id=user_id)
    else:
        return render_template(
            'browse_reviews.html', title='All Reviews', entries=entries,
            total=total, pages=pages, current_page=current_page,
            form=add_review_form)


"""
#  Update favorite functionallity Route
-------------------
This route enables signed in users to save/highlight their favorite reviews
alternativley remove higlight.
By getting the unique review post id & clicked/unclicked checkbox value from
the frontend. If the box is checked, adds the user ID to the faved_by list
array in database otherwise, removes the user ID from the faved_by list.
Sequentally returning a success response to the frontend.
"""


@app.route("/update_favorites/<review_id>/<is_fave>", methods=["GET", "POST"])
def update_favorites(review_id, is_fave):
    'user' in session
    # get the ID of the user
    user_id = users.find_one({'username': session['user'].lower()})['_id']
    if is_fave == "true":
        # Update/add user id to faved_by field array in reviews collection
        reviews.update({'_id': ObjectId(review_id)},
                       {'$addToSet': {'faved_by': user_id}})
    else:
        # Update/remove user id from faved_by field in reviews collection
        reviews.update({'_id': ObjectId(review_id)},
                       {'$pull': {'faved_by': user_id}})
    return Response(status=201, mimetype='update_favorites/html')


"""
#   Single review page
-------------------
 To display an individual review
"""


@app.route("/individual_view/<review_id>", methods=["GET"])
def individual_view(review_id):
    """ Signed in user with an added post is able to update and delete
    personal entries. """
    # Find specific review by Id
    individual_review = reviews.find_one({'_id': ObjectId(review_id)})
    if 'user' in session:
        users.find_one({'username': session['user'].lower()})
        ['username']
        return render_template(
            'individual_view.html', title='Individual review',
            individual_review=individual_review)
    return render_template(
        'individual_view.html', title='Individual review',
        individual_review=individual_review)


"""
#  Edit Review
-------------------
    Displays page that manages user updates, presented with pre-populated
    fields. The user is only enabled to update their own review entries,
    otherwise returning a 404 error.
"""


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """ Display edit form page """
    # Find the specific review to edit by Id
    individual_review = reviews.find_one({'_id': ObjectId(review_id)})
    add_review_form = AddReviewForm()
    category_name = categories.find()
    # Check if the selected review belongs to the signed in user
    if individual_review['added_by'] == session['user'].lower():
        # If the form data match the selected review data, send to front server
        add_review_form.brand_name.data = individual_review["brand_name"]
        add_review_form.product_review.data = (
            individual_review["product_review"])
        add_review_form.price.data = float(individual_review["price"])
        add_review_form.is_vegan.data = individual_review["is_vegan"]
        add_review_form.rating.data = individual_review["rating"]
        add_review_form.tags.data = ' '.join(individual_review["tags"])
        return render_template(
            'edit_review.html', title='Edit review',
            individual_review=individual_review, form=add_review_form,
            category_name=category_name)
    else:
        # Otherwise render error page
        return render_template('404.html', title="Page Not Found")


"""
#   About Us
-------------------

"""


@app.route('/about', methods=['GET', 'POST'])
def about():
    form = EmailForm()
    if form.validate_on_submit():
        # Check if email already exist in db
        existing_email = subscribes.find_one(
            {"email": request.form["email"].lower()})
        if existing_email:
            flash('This email already been registered', 'danger')
        else:
            email = {
                'email': request.form.get('email')
            }
            subscribes.insert_one(email)
            flash('Thank you for your subscription!', 'success')
            return render_template('about.html', title='About Us',
                                   form=form)
    return render_template('about.html', form=form)


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
        existing_user = users.find_one(
            {"username": request.form["username"].lower()})
        if existing_user:
            flash('Sorry, this username has been taken', 'danger')
            return redirect(url_for("register"))
        else:
            new_user = {
                "username": request.form["username"].lower(),
                "password": generate_password_hash(request.form["password"])
            }
            users.insert_one(new_user)

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
        existing_user = users.find_one(
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


@app.errorhandler(404)
def page_not_found(e):
    """Handels invalid URL inputs"""
    return render_template('404.html', title="Page Not Found"), 404
