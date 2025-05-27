from email.policy import default

from app.models.productCarts import CartsModel
from app import db
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from datetime import datetime as dt

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
    def get(self, id):
        cart = CartsModel.query.filter_by(id=id).first()
        if cart is None:
            abort(404, message="Cart not found")
        return cart

    @marshal_with(cartFields)
    def delete(self, id):
        cart = CartsModel.query.filter_by(id=id).first()
        if cart is None:
            abort(404, message="Cart not found")
        db.session.delete(cart)
        db.session.commit()
        carts = CartsModel.query.all()
        return carts

    @marshal_with(cartFields)
    def put(self, id):
        args = cart_args_put.parse_args()
        cart = CartsModel.query.filter_by(id=id).first()
        if cart is None:
            abort(404, message="Cart not found")
        elif cart.isPaid:
            abort(400, message="Paid cart")
        if cart.productList == "":
            cart.productList += args["productList"]
        else:
            cart.productList += "," + args['productList']
        cart.isPaid = args['isPaid']
        cart.lastUpdate = dt.now()
        db.session.commit()
        return cart


class Carts(Resource):
    @marshal_with(cartFields)
    def get(self):
        carts = CartsModel.query.all()
        return carts

    @marshal_with(cartFields)
    def post(self):
        args = cart_args_post.parse_args()
        cart = CartsModel(productList="", lastUpdate=dt.now(), createTime=dt.now(), owner=args['owner'])
        db.session.add(cart)
        db.session.commit()
        carts = CartsModel.query.all()
        return carts, 201


