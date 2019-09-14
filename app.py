from flask import Flask, render_template, redirect, request, url_for, flash, session
import os
from flask_pymongo import PyMongo, pymongo
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


# logout
@app.route('/logout')
def logout():
    if 'username' in session:
        session.clear()
        flash(f'You are now logged out', 'success')
    return redirect(url_for('login'))


# Profile
@app.route('/profile')
def profile():
    if 'username' in session:
        user = mongo.db.users.find_one({"username": session['username']})
        return render_template("profile.html", user=user, user_id=user['_id'])     
    return redirect(url_for('index'))


#edit profile
@app.route('/edit_profile/<user_id>')
def edit_profile(user_id):
    return render_template('editprofile.html', user=mongo.db.users.find_one(
    {'_id': ObjectId(user_id)}))


# update profile in db
@app.route('/update_profile/<user_id>', methods=['POST'])
def update_profile(user_id):
    hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
    mongo.db.users.replace_one(
        {'_id': ObjectId(user_id)},
        {'firstname': request.form['firstname'],
        'lastname': request.form['lastname'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': hashpass})
    flash(f'Your profile has been updated', 'success')        
    return redirect(url_for('profile'))


# delete profile from db
@app.route('/delete_profile/<user_id>')
def delete_profile(user_id):
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    session.clear()
    flash(f'Your profile has now been deleted', 'success')
    return redirect(url_for('profile'))

'''
Recipes
'''

# get all recipes
@app.route('/recipes', methods=['GET'])
def recipes():
    recipe = mongo.db.recipes

    recipes = mongo.db.recipes.find()

    offset = int(request.args['offset'])
    limit = int(request.args['limit'])
    recipe_count = recipe.count()

    starting_id = recipe.find().sort('_id', pymongo.ASCENDING)
    last_id = starting_id[offset]['_id']

    recipes = recipe.find({'_id' : {'$gte' : last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)

    output = []

    next_url = '/recipes?limit=' + str(limit) + '&offset=' + str(offset + limit)
    prev_url = '/recipes?limit=' + str(limit) + '&offset=' + str(offset - limit)  

    if 'username' in session:
        user = mongo.db.users.find_one({"username": session['username']})

        return render_template("recipes.html", recipes=recipes, recipe_count=recipe_count, next_url=next_url, prev_url=prev_url, limit=limit, offset=offset, user_id=user['_id'])

    return render_template("recipes.html", recipes=recipes, recipe_count=recipe_count, next_url=next_url, prev_url=prev_url, limit=limit, offset=offset,)


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

# insert recipe to db
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe =  mongo.db.recipes
    recipe.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))


'''
Diets
'''

# get all diets
@app.route('/diets')
def diets():
    return render_template('diets.html', diets=mongo.db.diets.find())

# add diet
@app.route('/add_diet')
def add_diet():
    return render_template('adddiet.html')

# insert diet to db
@app.route('/insert_diet', methods=['POST'])
def insert_diet():
    diets = mongo.db.diets
    diet_doc = {'diet_name': request.form.get('diet_name')}
    diets.insert_one(diet_doc)
    return redirect(url_for('diets'))

# edit diet
@app.route('/edit_diet/<diet_id>')
def edit_diet(diet_id):
    return render_template('editdiet.html', diet=mongo.db.diets.find_one(
    {'_id': ObjectId(diet_id)}))

# update diet in db
@app.route('/update_diet/<diet_id>', methods=['POST'])
def update_diet(diet_id):
    mongo.db.diets.replace_one(
        {'_id': ObjectId(diet_id)},
        {'diet_name': request.form.get('diet_name')})
    return redirect(url_for('diets'))

# delete diet in db
@app.route('/delete_diet/<diet_id>')
def delete_diet(diet_id):
    mongo.db.diets.delete_one({"_id": ObjectId(diet_id)})
    return redirect(url_for('diets'))


'''
Cuisine
'''

# get all cuisine
@app.route('/cuisine')
def cuisine():
    return render_template('cuisine.html', cuisine=mongo.db.cuisine.find())

# add cuisine
@app.route('/add_cuisine')
def add_cuisine():
    return render_template('addcuisine.html')


# insert cuisine to db
@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisine = mongo.db.cuisine
    cuisine_doc = {'cuisine_country': request.form.get('cuisine_country')}
    cuisine.insert_one(cuisine_doc)
    return redirect(url_for('cuisine'))


# edit cuisine
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    return render_template('editcuisine.html', cuisine=mongo.db.cuisine.find_one(
    {'_id': ObjectId(cuisine_id)}))


# update cuisine in db
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    mongo.db.cuisine.replace_one(
        {'_id': ObjectId(cuisine_id)},
        {'cuisine_country': request.form.get('cuisine_country')})
    return redirect(url_for('cuisine'))


# delete cuisine from db
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisine.delete_one({"_id": ObjectId(cuisine_id)})
    return redirect(url_for('cuisine'))


'''
Error pages
'''

# 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    if os.environ.get("DEVELOPMENT"):
        app.run(host=os.environ.get('IP'),
                port=os.environ.get('PORT'),
                debug=False)
    else:
        app.run(host=os.environ.get('IP'),
                port=os.environ.get('PORT'),
                debug=True)