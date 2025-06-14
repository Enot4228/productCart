from app.models.users import UsersModel, create_user
from app import db, bcrypt, app
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from flask import jsonify, request, make_response
from jwt import decode
from datetime import datetime


user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True)
user_args.add_argument("password", type=str, required=True)
user_args.add_argument("email", type=str, required=True)
user_args.add_argument("firstName", type=str, required=True)
user_args.add_argument("lastName", type=str, required=True)
user_args.add_argument("role", type=str, required=True)

userFields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "firstName": fields.String,
    "lastName": fields.String,
    "role": fields.String
}


class Users(Resource): # Get all users and post any new user with admin token
    @marshal_with(userFields)
    def get(self): # Get method
        token = request.headers.get("Authorization")
        try:
            payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['sub']
            expiration = payload['exp']
            user = UsersModel.query.get(int(current_user_id))
        except Exception as e:
            return make_response(jsonify({'message': "Unauthorized"}), 401)

        if user.role != "admin":
            return make_response(jsonify({'message': "Access denied"}), 403)

        if expiration < int(datetime.utcnow().timestamp()):
            return make_response(jsonify({'message': "Token expired"}), 401)

        users = UsersModel.query.all()
        print(users)
        return users, 200

    def post(self): # Post method
        token = request.headers.get("Authorization")
        try:
            payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['sub']
            expiration = payload['exp']
            user = UsersModel.query.get(int(current_user_id))
        except Exception as e:
            return make_response(jsonify({'message': "Unauthorized"}), 401)

        if user.role != "admin":
            return make_response(jsonify({'message': "Access denied"}), 403)

        if expiration < int(datetime.utcnow().timestamp()):
            return make_response(jsonify({'message': "Token expired"}), 401)

        args = user_args.parse_args()
        user_post = create_user(args)
        db.session.add(user_post)
        db.session.commit()
        return make_response(jsonify({'message': "User created"}), 201)

class User(Resource): # Get user by id with admin token
    @marshal_with(userFields)
    def get(self, id):
        token = request.headers.get("Authorization")
        try:
            payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['sub']
            expiration = payload['exp']
            user = UsersModel.query.get(int(current_user_id))
        except Exception as e:
            return make_response(jsonify({'message': "Unauthorized"}), 401)

        if user.role != "admin":
            return make_response(jsonify({'message': "Access denied"}), 403)

        if expiration < int(datetime.utcnow().timestamp()):
            return make_response(jsonify({'message': "Token expired"}), 401)

        user = UsersModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user
