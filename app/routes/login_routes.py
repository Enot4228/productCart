from flask_restful import Resource, reqparse
from app.models.users import UsersModel
from app import bcrypt, app
from flask import jsonify, make_response
from jwt import encode
import datetime

login_args = reqparse.RequestParser()
login_args.add_argument("username", type=str, required=True)
login_args.add_argument("password", type=str, required=True)

class Login(Resource):

    def get(self):
        args = login_args.parse_args()
        user = UsersModel.query.filter_by(username=args['username']).first()
        if user is None or not bcrypt.check_password_hash(user.hashedPassword, args['password']):
            return make_response(jsonify({"message": "Invalid credentials"}), 401)

        token = encode(
            {
                "sub": str(user.id),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            },
             app.config['SECRET_KEY'],
             algorithm='HS256'
        )

        return make_response(jsonify({"token": token}), 200)