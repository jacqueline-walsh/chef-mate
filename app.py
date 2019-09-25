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

# collections from Database
users_coll = mongo.db.users
recipes_coll = mongo.db.recipes
diets_coll = mongo.db.diets
cuisine_coll = mongo.db.cuisine
difficulty_coll = mongo.db.difficulty


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
        existing_user = users_coll.find_one({'username' : request.form['username']})    

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users_coll.insert_one({
                'firstname': request.form['firstname'].capitalize(),
                'lastname': request.form['lastname'].capitalize(),    
                'email': request.form['email'],                            
                'username': request.form['username'],
                'password': hashpass,
                'admin': False})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            flash(f"Sorry username, {request.form['username']} already exists", 'danger')

    return render_template('register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        login_user = users_coll.find_one({'username' : request.form['username']})

        if login_user is not None:
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
        user = users_coll.find_one({"username": session['username']})
        return render_template("profile.html", user=user, user_id=user['_id'])     
    return redirect(url_for('index'))


#edit profile
@app.route('/edit_profile/<user_id>')
def edit_profile(user_id):
    return render_template('editprofile.html', user=users_coll.find_one({'_id': ObjectId(user_id)}))


# update profile in db
@app.route('/update_profile/<user_id>', methods=['POST'])
def update_profile(user_id):
    hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
    users_coll.replace_one(
        {'_id': ObjectId(user_id)},
        {'firstname': request.form['firstname'].capitalize(),
        'lastname': request.form['lastname'].capitalize(),
        'username': request.form['username'],
        'email': request.form['email'],
        'password': hashpass})
    flash(f'Your profile has been updated', 'success')        
    return redirect(url_for('profile'))


# delete profile from db
@app.route('/delete_profile/<user_id>')
def delete_profile(user_id):
    users_coll.delete_one({"_id": ObjectId(user_id)})
    session.clear()
    flash(f'Your profile has now been deleted', 'success')
    return redirect(url_for('profile'))

'''
Recipes
'''

# get all recipes
@app.route('/recipes')
def recipes():
    recipe = recipes_coll

    the_diet = diets_coll.find()
    the_cuisine = cuisine_coll.find()

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
        user = users_coll.find_one({"username": session['username']})

        return render_template("recipes.html", recipes=recipes, diets=the_diet, cuisine=the_cuisine, recipe_count=recipe_count, next_url=next_url, prev_url=prev_url, limit=limit, offset=offset, user_id=user['_id'])

    return render_template("recipes.html", recipes=recipes, diets=the_diet, cuisine=the_cuisine,  recipe_count=recipe_count, next_url=next_url, prev_url=prev_url, limit=limit, offset=offset)


# search recipes
@app.route('/search')
def search_recipes():
    recipes_coll.create_index([( 'recipe_title', pymongo.TEXT )], name="text")
    db_query = request.args['db_query']
    recipes = recipes_coll.find({'$text': {'$search': db_query}}).limit(6)
    return render_template("search.html", recipes=recipes)    

# filter by cuisine
@app.route('/search_cuisine/<cuisine_country>')
def search_cuisine(cuisine_country):
    recipes = recipes_coll.find({'recipe_cuisine' : cuisine_country})
    return render_template("search_cuisine.html", recipes=recipes)    

# filter by diet
@app.route('/search_diet/<diet>')
def search_diet(diet):
    recipes = recipes_coll.find({'recipe_diet' : diet})
    return render_template("search_diet.html", recipes=recipes)                                 

# get a single recipe
@app.route('/recipe/<recipe_id>')
def recipe(recipe_id):
    recipe=recipes_coll.find_one({'_id': ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=recipe)

# add recipe
@app.route('/add_recipe/')
def add_recipe():
    the_diet = diets_coll.find()
    the_cuisine = cuisine_coll.find()
    the_difficulty = difficulty_coll.find()
    return render_template('addrecipe.html',
                           diets=the_diet, cuisine=the_cuisine, difficulty=the_difficulty)

# insert recipe to db
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipe =  recipes_coll
    recipe.insert_one(
        {
        "recipe_title" : request.form.get('recipe_title').capitalize(),
        "recipe_diet" : request.form.get('recipe_diet').capitalize(),
        "recipe_ingredients" : request.form.getlist('recipe_ingredients'),
        "recipe_steps" : request.form.getlist('recipe_steps'),
        "recipe_prep" : int(request.form.get('recipe_prep')),
        "recipe_cook" : int(request.form.get('recipe_cook')),
        "recipe_difficulty" : request.form.get('recipe_difficulty'),
        "recipe_servings" : int(request.form.get('recipe_servings')),
        "recipe_cuisine" : request.form.get('recipe_cuisine').capitalize(),
        "recipe_credits" : request.form.get('recipe_credits'),
        "recipe_image" : request.form.get('recipe_image')
        }            
    )
    flash(f"Recipe added. Thank you!", 'success')
    return redirect(url_for('recipes', limit=6, offset=0))

# edit recipe
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe = recipes_coll.find_one({"_id": ObjectId(recipe_id)})
    the_diet = diets_coll.find()
    the_cuisine = cuisine_coll.find()
    the_difficulty = difficulty_coll.find()
    return render_template('editrecipe.html', recipe=recipe, diets=the_diet, cuisine=the_cuisine, difficulty=the_difficulty)

# update recipe in db
@app.route('/update_recipes/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes_coll.update_one(
        {'_id': ObjectId(recipe_id)},
        {'$set':
            {           
            "recipe_title" : request.form.get('recipe_title').capitalize(),
            "recipe_diet" : request.form.get('recipe_diet').capitalize(),
            "recipe_ingredients" : request.form.getlist('recipe_ingredients'),
            "recipe_steps" : request.form.getlist('recipe_steps'),
            "recipe_prep" : int(request.form.get('recipe_prep')),
            "recipe_cook" : int(request.form.get('recipe_cook')),
            "recipe_difficulty" : request.form.get('recipe_difficulty'),
            "recipe_servings" : int(request.form.get('recipe_servings')),
            "recipe_cuisine" : request.form.get('recipe_cuisine').capitalize(),
            "recipe_credits" : request.form.get('recipe_credits'),
            "recipe_image" : request.form.get('recipe_image')
            }
        }
    )
        
    flash(f"Recipe has been updated. Thank you!", 'success')
    return redirect(url_for('recipe', recipe_id=recipe_id))

# delete recipe in db
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipes_coll.delete_one({"_id": ObjectId(recipe_id)})
    flash(f"Recipe deleted", 'success')
    return redirect(url_for('recipes', limit=6, offset=0))

# search all recipes


'''
Diets
'''

# get all diets
@app.route('/diets')
def diets():
    return render_template('diets.html', diets=diets_coll.find())

# add diet
@app.route('/add_diet')
def add_diet():
    return render_template('adddiet.html')

# insert diet to db
@app.route('/insert_diet', methods=['POST'])
def insert_diet():
    diets = diets_coll
    diet_doc = {'diet_name': request.form.get('diet_name').capitalize()}
    diets.insert_one(diet_doc)
    flash(f"diet added. Thank you!", 'success')
    return redirect(url_for('diets'))

# edit diet
@app.route('/edit_diet/<diet_id>')
def edit_diet(diet_id):
    return render_template('editdiet.html', diet=diets_coll.find_one(
    {'_id': ObjectId(diet_id)}))

# update diet in db
@app.route('/update_diet/<diet_id>', methods=['POST'])
def update_diet(diet_id):
    diets_coll.replace_one(
        {'_id': ObjectId(diet_id)},
        {'diet_name': request.form.get('diet_name')})
    flash(f"Diet has been updated. Thank you!", 'success')
    return redirect(url_for('diets'))

# delete diet in db
@app.route('/delete_diet/<diet_id>')
def delete_diet(diet_id):
    diets_coll.delete_one({"_id": ObjectId(diet_id)})
    flash(f"Diet deleted", 'success')
    return redirect(url_for('diets'))


'''
Cuisine
'''

# get all cuisine
@app.route('/cuisine')
def cuisine():
    return render_template('cuisine.html', cuisine=cuisine_coll.find())

# add cuisine
@app.route('/add_cuisine')
def add_cuisine():
    return render_template('addcuisine.html')


# insert cuisine to db
@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisine = cuisine_coll
    cuisine_doc = {'cuisine_country': request.form.get('cuisine_country').capitalize()}
    cuisine.insert_one(cuisine_doc)
    flash(f"Cuisine added. Thank you!", 'success')
    return redirect(url_for('cuisine'))


# edit cuisine
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    return render_template('editcuisine.html', cuisine=cuisine_coll.find_one(
    {'_id': ObjectId(cuisine_id)}))


# update cuisine in db
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    cuisine_coll.replace_one(
        {'_id': ObjectId(cuisine_id)},
        {'cuisine_country': request.form.get('cuisine_country')})
    flash(f"Cuisine has been updated. Thank you!", 'success')
    return redirect(url_for('cuisine'))


# delete cuisine from db
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    cuisine_coll.delete_one({"_id": ObjectId(cuisine_id)})
    flash(f"Cuisine Deleted. Thank you!", 'success')
    return redirect(url_for('cuisine'))


'''
Dashboard Page
'''

# dashboard for d3.js charts
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

'''
Error page
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