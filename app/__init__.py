from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    api = Api(app)
    db.init_app(app)

    from .routes.routes import Cart, Carts
    api.add_resource(Cart, '/api/cart/<int:id>')
    api.add_resource(Carts, '/api/carts')

    return app, db