import sys

sys.path.append('..')

from voiceserver import app
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    salt = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.login


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    cook = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(15))
    hard = db.Column(db.String(15))

    def __repr__(self):
        return '<Recipe %r>' % self.title


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(30), nullable=False)


class UsersGroups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class UsersRecipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))


if __name__ == '__main__':
    manager.run()
