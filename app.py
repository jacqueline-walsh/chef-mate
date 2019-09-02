from flask import Flask, render_template, redirect, request, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
# from secret import MONGO_URI

app = Flask(__name__)


app.config['MONGO_DBNAME'] = os.environ.get('chef_mateDB')
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_recipes')
def get_recipes():
    return render_template("get_recipes.html",
                           recipes=mongo.db.recipes.find())


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
             port=int(os.environ.get('PORT')))
    # app.run(debug=True)