from src.database import db
from src.database.models import User


# Create a new user
def create_user(data):
    _username = data.get('username')
    _email = data.get('email')
    _password = data.get('password')
    user = User(_username, _email, _password)
    db.session.add(user)
    db.session.commit()


# Update an existing user
def update_user(user_id, data):
    user = User.query.filter(User.id == user_id).one()
    user.username = data.get('username')
    user.email = data.get('email')
    user.password = data.get('password')
    db.session.add(user)
    db.session.commit()


# Delete an existing user
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).one()
    db.session.delete(user)
    db.session.commit()