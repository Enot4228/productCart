from flask_restful import Resource
from app.models.users import UsersModel
from flask import jsonify, make_response
from app import db, bcrypt
from app.routes.user_routes import user_args

class Register(Resource):

    def post(self):
        args = user_args.parse_args()
        if args['role'] == "admin" and UsersModel.query.filter_by(role='admin').count() >= 3:
            return jsonify({'message': "Too much admins. Change role im registration form"})
        user = UsersModel(username=args['username'], email=args['email'], firstName=args['firstName'],
                          lastName=args['lastName'], hashedPassword=bcrypt.generate_password_hash(args['password']).decode('utf-8'),
                          role=args['role'])
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({"message": "User registered successfully"}), 201)