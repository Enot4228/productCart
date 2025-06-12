from app.models.users import UsersModel
from app import db, bcrypt, app
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from flask import jsonify, request, make_response
from jwt import decode
from datetime import datetime


user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True)
user_args.add_argument("password", type=str, required=True) # Assume that the password will be hashed
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



#ToDo remove code duplications
#ToDo Review all fucntions
#ToDo test all functions
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
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

    @marshal_with(userFields)
    def post(self):
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
        user_post = UsersModel(username=args['username'], email=args['email'], firstName=args['firstName'], lastName=args['lastName'],
                          hashedPassword=bcrypt.generate_password_hash(args['password']).decode('utf-8'), role=args['role'])
        db.session.add(user_post)
        db.session.commit()
        return make_response(jsonify({'message': "User created"}), 201)

class User(Resource):
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

int(datetime.utcnow().timestamp())