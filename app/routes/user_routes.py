from app.models.users import UsersModel
from app.models.auth import AuthModel
from app import db
from flask_restful import Resource, reqparse, marshal_with, abort, fields
from datetime import datetime

user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, required=True)
user_args.add_argument("password", type=str, required=True) # Assume that the password will be hashed
user_args.add_argument("email", type=str, required=True)
user_args.add_argument("firstName", type=str, required=True)
user_args.add_argument("lastName", type=str, required=True)

userFields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "firstName": fields.String,
    "lastName": fields.String
}

#ToDo Add Authentication with admin user only
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UsersModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UsersModel(username=args['username'], email=args['email'], firstName=args['firstName'], lastName=args['lastName'])
        auth = AuthModel(username=args['username'], password=args['password'])
        db.session.add(user)
        db.session.add(auth)
        db.session.commit()
        return user, 200

class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UsersModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user

