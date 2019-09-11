from flask import Flask, render_template, redirect, request, url_for, flash, session
# import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import env as config


app = Flask(__name__)

# configuration of Database
app.config['MONGO_URI'] = config.MONGO_URI
app.config['SECRET_KEY'] = config.SECRET_KEY

mongo = PyMongo(app)


# routing for pages
'''
home page
'''
@app.route('/')
def index():
    if 'username' in session:
        flash(f"You are logged in as {session['username']}", 'success')
    return render_template('index.html')


"""
Users / Log-in / Register
"""
# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users 
        existing_user = users.find_one({'username' : request.form['username']})    

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'firstname': request.form['firstname'],
                'lastname': request.form['lastname'],    
                'email': request.form['email'],                            
                'username': request.form['username'],
                'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            flash(f"Sorry username, {request.form['username']} already exists", 'danger')

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        else:
            flash(f"Sorry username or password invalid", 'danger')   

    return render_template('login.html')

'''
receipes
'''
# get all recipes
@app.route('/recipes')
def recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())

# get a single recipe
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    return render_template("recipe.html", recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))

# add recipe
@app.route('/add_recipe')
def add_recipe():
    the_diet = mongo.db.diets.find()
    the_cuisine = mongo.db.cuisine.find()
    return render_template('addrecipe.html',
                           diets=the_diet, cuisine=the_cuisine)


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe =  mongo.db.recipes
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))


'''
Diets
'''

@app.route('/diets')
def diets():
    return render_template('diets.html', diets=mongo.db.diets.find())

@app.route('/add_diet')
def add_diet():
    return render_template('adddiet.html')


@app.route('/insert_diet', methods=['POST'])
def insert_diet():
    diets = mongo.db.diets
    diet_doc = {'diet_name': request.form.get('diet_name')}
    diets.insert_one(diet_doc)
    return redirect(url_for('diets'))


@app.route('/edit_diet/<diet_id>')
def edit_diet(diet_id):
    return render_template('editdiet.html', diet=mongo.db.diets.find_one(
    {'_id': ObjectId(diet_id)}))


@app.route('/update_diet/<diet_id>', methods=['POST'])
def update_diet(diet_id):
    mongo.db.diets.replace_one(
        {'_id': ObjectId(diet_id)},
        {'diet_name': request.form.get('diet_name')})
    return redirect(url_for('diets'))


@app.route('/delete_diet/<diet_id>')
def delete_diet(diet_id):
    mongo.db.diets.delete_one({"_id": ObjectId(diet_id)})
    return redirect(url_for('diets'))


'''
Cuisine
'''

@app.route('/cuisine')
def cuisine():
    return render_template('cuisine.html', cuisine=mongo.db.cuisine.find())

@app.route('/add_cuisine')
def add_cuisine():
    return render_template('addcuisine.html')


@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisine = mongo.db.cuisine
    cuisine_doc = {'cuisine_country': request.form.get('cuisine_country')}
    cuisine.insert_one(cuisine_doc)
    return redirect(url_for('cuisine'))


@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    return render_template('editcuisine.html', cuisine=mongo.db.cuisine.find_one(
    {'_id': ObjectId(cuisine_id)}))


@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    mongo.db.cuisine.replace_one(
        {'_id': ObjectId(cuisine_id)},
        {'cuisine_country': request.form.get('cuisine_country')})
    return redirect(url_for('cuisine'))


@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisine.delete_one({"_id": ObjectId(cuisine_id)})
    return redirect(url_for('cuisine'))


if __name__ == '__main__':
    # app.run(host=os.environ.get('IP'),
    #          port=int(os.environ.get('PORT')))
    app.run(debug=True)