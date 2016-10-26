from src.database import db
from src.database.models import Recipe


# Create a new recipe
def create_recipe(data):
  _name = data.get('name')
  _ingredients = data.get('ingredients')
  _imageUrl = data.get('imageUrl')
  recipe = Recipe(_name, _ingredients, _imageUrl)
  # db.session.add(user)
  # db.session.commit()
  return recipe


# Try and find an existing recipe
def get_recipe(recipe_id):
  recipe = Recipe.query.filter(Post.id == id).one()
  if recipe is None:
    return "Could not find recipe with id: " + id
  return recipe


# Update an existing recipe
def update_recipe(recipe_id, data):
  recipe = Recipe.query.filter(Recipe.id == recipe_id).one()
  # db.session.add(user)
  # db.session.commit()


# Delete an existingrecipeuser
def delete_recipe(recipe_id):
  recipe = Recipe.query.filter(Recipe.id == recipe_id).one()
  # db.session.delete(user)
  # db.session.commit()