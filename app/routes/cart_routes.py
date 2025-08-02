from app.models.productCarts import CartsModel
from app import db, app
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from datetime import datetime as dt
from flask import jsonify, request, make_response
from jwt import decode
from app.models.users import UsersModel


cart_args_post = reqparse.RequestParser()
cart_args_post.add_argument("owner", type=str, required=True)

cart_args_put = reqparse.RequestParser()
cart_args_put.add_argument("owner", type=str, required=True)
cart_args_put.add_argument("productList", type=str, required=True)
cart_args_put.add_argument('isPaid', type=bool, default=False)

cartFields = {
    "id": fields.Integer,
    "productList": fields.String,
    "lastUpdate": fields.DateTime,
    "createTime": fields.DateTime,
    "owner": fields.String,
    "isPaid": fields.Boolean,
}

class Cart(Resource):
    @marshal_with(cartFields)
    def get(self, id): # ToDo test token auth work
        token = request.headers.get("Authorization")
        try:
            payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['sub']
            expiration = payload['exp']
            user = UsersModel.query.get(id=int(current_user_id))
        except Exception as e:
            return make_response(jsonify({'message': "Unauthorized"}), 401)

        if user.role != "admin":
            return make_response(jsonify({'message': "Access denied"}), 403)

        if expiration < int(dt.utcnow().timestamp()):
            return make_response(jsonify({'message': "Token expired"}), 401)

        cart = CartsModel.query.filter_by(id=id).first()
        if cart is None:
            abort(404, message="Cart not found")
        return cart

    @marshal_with(cartFields)
    def delete(self, id): # ToDo test token auth work
        token = request.headers.get("Authorization")
        try:
            payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['sub']
            expiration = payload['exp']
            user = UsersModel.query.get(id=int(current_user_id))
        except Exception as e:
            return make_response(jsonify({'message': "Unauthorized"}), 401)

        if user.role != "admin":
            return make_response(jsonify({'message': "Access denied"}), 403)

        if expiration < int(dt.utcnow().timestamp()):
            return make_response(jsonify({'message': "Token expired"}), 401)

        cart = CartsModel.query.filter_by(id=id).first()
        if cart is None:
            abort(404, message="Cart not found")
        db.session.delete(cart)
        db.session.commit()
        carts = CartsModel.query.all()
        return carts


class Carts(Resource):
    @marshal_with(cartFields)
    def get(self): # ToDo add admin token auth
        carts = CartsModel.query.all()
        return carts

    @marshal_with(cartFields)
    def post(self): # Todo add user token create cart
        args = cart_args_post.parse_args()
        cart = CartsModel(productList="", lastUpdate=dt.now(), createTime=dt.now(), owner=args['owner'])
        db.session.add(cart)
        db.session.commit()
        carts = CartsModel.query.all()
        return carts, 201

    @marshal_with(cartFields)
    def put(self):  # ToDo test update cart with user token
        args = cart_args_put.parse_args()
        token = request.headers.get("Authorization")
        try:
            payload = decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = payload['sub']
            expiration = payload['exp']
            user = UsersModel.query.get(id=int(current_user_id))
        except:
            return make_response(jsonify({'message': "Unauthorized"}), 401)

        if expiration < int(dt.utcnow().timestamp()):
            return make_response(jsonify({'message': "Token expired"}), 401)

        cart = CartsModel.query.filter_by(owner=user.username, isPaid=False).first()
        if cart is None:
            abort(404, message="Cart not found")

        if cart.productList == "":
            cart.productList += args['productList']
        else:
            cart.productList += ',' + args['productList']
        cart.isPaid = args['isPaid']
        cart.lastUpdate = dt.now()
        db.session.commit()

        # cart = CartsModel.query.filter_by(id=id).first()
        # if cart is None:
        #     abort(404, message="Cart not found")
        # elif cart.isPaid:
        #     abort(400, message="Paid cart")
        # if cart.productList == "":
        #     cart.productList += args["productList"]
        # else:
        #     cart.productList += "," + args['productList']
        # cart.isPaid = args['isPaid']
        # cart.lastUpdate = dt.now()
        # db.session.commit()
        return cart


