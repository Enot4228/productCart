from flask_restful import Resource
from app.models.users import UsersModel, create_user
from flask import jsonify, make_response
from app import db
from app.routes.user_routes import user_args

class Register(Resource):

    def post(self):
        args = user_args.parse_args()
        if args['role'] == "admin" and UsersModel.query.filter_by(role='admin').count() >= 3:
            return make_response(jsonify({'message': "Too much admins. Change role im registration form"}), 400)
        user = create_user(args)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "User registered successfully"}), 201)