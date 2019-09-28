# ChefMate - Recipe Manager

<img src="https://code-institute.s3-eu-west-1.amazonaws.com/chef-mate/mac-screen.jpg" alt="screenshot of site" width="100%">


This project is to provide a one stop shop for all your favourite recipes.  Users can experience a rich environment full of colourful imagery, a list of ingredients to shop for and the step by step instructions on how to make that perfect meal.  As well as being able to store and organise your own special recipes, you can check out other inspirational ideas from others and rate to give feedback.  Search for a typical dish by country, dietary need or just by recipe title. Visit the data section for a dashboard of dynamic graphs.  This is an app that you won't be able to live without!

- [Live link](http://chefmate-manager.herokuapp.com/)
- [Github Link](https://github.com/jacqueline-walsh/chef-mate)
 
## UX

ChefMate is for anyone leading a busy life, that needs to store their favourite recipes, but also when time permits look for other exciting ideas to create a new masterpiece dish in the kitchen.  

The site has been designed with the busy user in mind, with a clean look and links to move around the site without having to use the browsers back link. 

Only registered users can save their recipes and become part of a group building on cuisine and dietary needs.  

The colorful dashboard gives all users data for every recipe and contains 2 piecharts and 2 bar charts.

### User Story

The user is a first time visitor to the site:
- User looks at the main navbar and see they are able to view all recipes, login, register or go to dashboard.
- User click on all the recipes and sees there are buttons to go to each recipe for the full recipe details.
- User likes the idea of trying out the recipe for buffalo wings so clicks on the image.
- User now has a list of full ingredients, steps on how to make the dish and can even like or dislike the recipe results after trying out.  
- The user looks at the prep and cook time and realises they do not have time to make this dish so goes back to all recipes to look again.
- User remembers that they have a themed dinner party to arrange for Friday so click on the cuisine filter to select only Chinese dishes.
- Liking the Cashew Chicken stir fry dish, the users prints out the recipe so that they can purchase all ingredients needed at the supermarket.
- User visits the page again after cooking the Cashew Chicken stir fry dish which went down a treat at the dinner party and gives it a thumbs up.
- After trying out the site the user decides to register and become part of the community and store and share their own favorite recipes online.

### Mockups

Mockups have been created for each page with the aid of Balsamiq a wireframe tool. 

[Wireframe - Desktop](https://github.com/jacqueline-walsh/chef-mate/tree/master/wireframes)

## Existing Features

### Homepage

This is a large feature page the gives an insight to what the site is all about.

### All Recipes

- Overall view of the recipes available to all users
- Pagination set to hold only 6 recipes per page
- 2 x Select fields at the top of the recipes page so all users can filter recipes by either country of cuisine, or by dietry need
- Search feature so all users can search recipes by a word in the recipe title
- Each recipe can be selected by either clicking a button or image to see the full recipe image page.  All users can access this
- Once logged in you can see a clickable 'my recipe book' which will take the logged in user to all their recipes added

### Single Recipe 
- All users can view the individual recipes details which show the following details:
    - print button to print recipe ingredients, image and steps
    - image of dish
    - cuisine
    - diet
    - both prep and cook time
    - username of person who added recipe
    - ratings.  Thumbs up or down.  A widget from [rate my widget](https://rating-widget.com/)
    - If user is logged in or admin they will see edit and delete buttons.  Only credited user can edit or delete their own recipes but admin can edit and delete all recipes
    - list of ingredients needed
    - list of steps required to make the dish

### Login Page

- User can log in with username and password.  Validation has been implemented so that the user has to enter correct details as well as both fields required
- Link to registration page if user realises they need to set up an account.

### Register Page

- Validation has been used on all fields and all fields are required
- User cannot register with a username already taken, they will receive a message to try another username
- Confirm password will not match until all characters match with password field

### Dashboard
- All users can see the dashboard
- piechart depicting number of recipes by cuisine (country of dish)
- piechart depicting number of recipes by dietary type
- bar graph showing difficulty of recipes, shown by country
- bar graph total of prep / cook time needed per country of cuisine

### Add Recipe
- Only available to registered users
- all fields required apart from the image field, there is a default image available if no image available.  Credit field is automatically completed with the username of user logged in
- ingredients and steps both have dynamic fields to add more fields when needed and delete unnecessary fields
- 3 select fields where cuisine, dietry type and diffculty of dish can be selected
- links to create more countries for the cuisine list or add more dietry types are available.  Only admin can edit or delete cuisine and dietry fields

### Profile 
- User can view their own profile details

### Logout
- User can logout at any time

### Features Left to Implement
- Social media could be implemented to allow sharing of recipes to various media
- User being able to save recipes to their own "my recipes" page

## Technologies Used

Many languages, frameworks and libraries have been used on this project:

### Repository
[github](https://github.com/jacqueline-walsh/chef-mate) - Github has been used throughout the project. At each stage throughout the development of the application the changes have been pushed to the repostory to provide a history of commits and changes of each new feature

### Frontend
- HTML5 - Semantic HTML5 has been implemented thoughout the site
- CSS3 - used for the styling of the site and to provide a more visually pleasing effect.
- Javascript - For dynamic interactive fields and other features included in the site
- [JQuery](https://jquery.com) - the project uses **JQuery** to simplify DOM manipulation.
- [bootstrap](https://getbootstrap.com/) - Bootstrap was implemented to assist with site layout and responsive design 
- [Font Awesome](https://fontawesome.com/) - visual icons have been used from Font Awesome
- [Google Fonts](https://fonts.google.com/) - for the typeography of the site
- [AWS](https://aws.amazon.com/) - storage for all images so to keep the site as light as possible.  Also where possible all links are CDN

### Backend
- [Mongo Atlas](https://www.mongodb.com/cloud/atlas) - Database and implementing of graphs for the site
- Flask - a Python framework.  The whole application has been built on this framework
- PyMongo - a Object Relationship Mapper (ORM) for querying the Mongodb Atlas database
- Bcrypt - for hash of password for input to database

### Hosting
- [Heroku](https://www.heroku.com) - the application has been hosted on heroku


## Testing

Throughout the development each section / function and action was tested visually within the chrome browser to ensure that the feature was implemented correctly.  Bugs with variables were initially investigated via either a print() or by using ipdb, (to install use `$ pip3 install ipdb`) and `import ipdb; ipdb.set_trace()` placed at the source of the problem.  Both solutions output to the terminal.

[W3C html Validation](https://validator.w3.org) - all html files have been validate, however errors were found due to the jinja templating
[W3C CSS Validation](https://jigsaw.w3.org/css-validator/) - all style sheets have been validated

For testing GET and POST request between the application and database [Postman](https://www.getpostman.com) 

Visual Studio Code was the text editor of choice for the application. The following extensions were installed for the project to assist testing and debugging:

- Python - Linting, Debugging (multi-threaded, remote), Intellisense, code formatting, refactoring, unit tests, snippets, and more
- Jinja template language support for Visual Studio Code
- Flask snippets collections - Initially ported from PyCharm, TextMate, SublimeText and other editors/IDEs

The site has been intensively user tested to ensure the following:

- all links are fully functioning
- validation on forms prompting and working correctly
- registration return error message if username already in database
- password and password confirm return match if same
- mobile view are in good design and order
- user experience has been enjoyable experience with no frustration of getting lost or confused
- flash messages appear and are correctly displayed
- data is being received and stored correctly on the database

## Deployment

Heroku has been used for the deployment of the site, see settings below for further details:

Free cloud hosting platform which simplify the deployment process.

### Heroku Settings added Config Vars

KEY | VALUE
--- | -----
IP | 0.0.0.0 |
PORT | 5000 |
MONGO_URI | link to db |
SECRET_KEY | SECRET_KEY |

### Deploy to Heroku via Terminal
- Go to heroku and create a new app
- In terminal carry out the following steps
    - $ heroku login
    - $ git add .
    - $ git commit -m "message for deployment"
    - $ git push heroku master
- Heroku then launches the application and provides a link to the new live site
- Go to heroku and select more tab in top right and click on Restart All Dynos
- Select tab to Open app in browser next to more tab.

## Deployment from Github to localhost

*Local deployment relies on a database connection and therefore you will need to set up your own environment*

1. Clone / download the repository at [https://github.com/jacqueline-walsh/chef-mate](https://github.com/jacqueline-walsh/chef-mate)
2. Install required packages:
    - `pip install -r requirements.txt`
3. In app.py ensure following settings:
   - IP `0.0.0.0`
   - PORT `5000`
   - MONGO_URI `Your database connection`
   - SECRET_KEY `secret_key`
4. To run application:
    - $ python3 app.py
5. This should now run on your local environment on `http://127.0.0.1:5000/`

## Credits

- [Ratings on recipe page](https://rating-widget.com/)

### Content
- Images and details of recipes from [BBC Good Food](https://www.bbcgoodfood.com/recipes)

### Media
- The photos used in this site were obtained from ...
    - [Logo](https://svgsilh.com/ffffff/image/3418134.html) — original image pixel bay
    - [Background-image](http://www.teamopenoffice.org/topk/cooking-wallpaper)
    - [Favicon](https://www.freepngimg.com/png/29422-cooking-image/icon)
    - [Login / registration background wallpaper](https://backgrounddownload.com/cooking-tools-seamless-pattern-background-set/)
    - [Ingredients background](https://pngtree.com/element/down?id=MzE5NzI2NQ==&type=1&t=3)
    - [Default recipe image](https://imgbin.com/png/bTA0mEdN/cloche-computer-icons-plate-png)

### Acknowledgements

- I received inspiration for this project google search for all recipe sites
