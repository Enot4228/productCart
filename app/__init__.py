from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '(w*+t8$2=(ev&h5clwcz8-)a1%8!1hucd_d#qw0yu%h4r6jq$='
api = Api(app)
db.init_app(app)
bcrypt.init_app(app)

from .routes.cart_routes import Cart, Carts
from .routes.user_routes import Users, User
from .routes.login_routes import Login
from .routes.register_routes import Register
api.add_resource(Cart, '/api/cart/<int:id>') # Admin only
api.add_resource(Carts, '/api/carts')
api.add_resource(Users, '/api/users') # Admin only
api.add_resource(User, '/api/users/<int:id>') # Admin only
api.add_resource(Login, '/api/login')
api.add_resource(Register, '/api/register')
