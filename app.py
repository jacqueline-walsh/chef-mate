from flask import Flask, render_template, redirect, request, url_for, flash
from forms import RegistrationForm, LoginForm
# import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import env as config

app = Flask(__name__)

# configuration of Database
app.config['MONGO_DBNAME'] = 'task_manager'
app.config['MONGO_URI'] = config.MONGO_URI
app.config['SECRET_KEY'] = config.SECRET_KEY

mongo = PyMongo(app)

# routing for pages
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes')
def recipes():
    return render_template("recipes.html",
                           recipes=mongo.db.recipes.find())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    if form.username.data == 'jacqann' and form.password.data == 'password':
      flash('You have been logged in!', 'success')
      return redirect(url_for('index'))
    else:
      flash('login Unsuccessful.  Please check username and password!', 'danger')
  return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),
    #          port=int(os.environ.get('PORT')))
    app.run(debug=True)