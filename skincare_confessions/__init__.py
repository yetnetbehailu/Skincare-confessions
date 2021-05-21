import os
from flask import Flask
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["Mongo_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

app.config['SECRET_KEY'] = 'SECRET_KEY'

mongo = PyMongo(app)

from skincare_confessions import routes
