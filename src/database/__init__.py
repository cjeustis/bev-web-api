from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Initialize the database with a user and a couple recipes
# for testing purposes
def init_database():
  reset_database()
  from src.database.models import User, Recipe, Ingredients
  from src.api.users.business import create_user, create_recipe, update_recipe

  # Create a generic admin user 
  admin_user = {
    "username": "admin",
    "password": "admin",
    "email": "admin@email.com"
  }
  create_user(admin_user)
  recipe1 = {
    "imageUrl": "http://liquor.s3.amazonaws.com/wp-content/uploads/2012/06/bulleit-perfect-manhattan1.jpg",
    "ingredients": [
      {
        'name': 'Whiskey',
        'name': 'Sweet Vermouth',
        'name': 'Bitters'
      }
    ],
    "name": "Manhattan",
  }
  ingsForRecipe1 = [
    {
      'name': 'Whiskey',
      'name': 'Sweet Vermouth',
      'name': 'Bitters'
    }
  ]
  recipe2 = {
    "imageUrl": "http://therumpus.net/wp-content/uploads/2015/06/RiG6yG9oT.png",
    "ingredients": [
      {
        'name': 'Tequila',
        'name': 'Vodka',
        'name': 'Rum',
        'name': 'Gin',
        'name': 'Raspberry Liqueur'
      }
    ],
    "name": "Grateful Dead",
  }
  ingsForRecipe2 = [
    {
      'name': 'Tequila',
      'name': 'Vodka',
      'name': 'Rum',
      'name': 'Gin',
      'name': 'Raspberry Liqueur'
    }
  ]
  create_recipe(1, recipe1)
  update_recipe(1, 1, recipe1)
  create_recipe(1, recipe2)
  update_recipe(1, 2, recipe2)
  

def reset_database():
  db.drop_all()
  db.create_all()