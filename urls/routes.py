#ToDo fix ImportError of circular import
from models.productCarts import CartsModel, db
from flask_restful import Resource, reqparse, marshal_with, fields, abort
from datetime import datetime as dt

cart_args = reqparse.RequestParser()
cart_args.add_argument("owner", type=str, required=True)

class Cart(Resource):
    @marshal_with(cart_args)
    def get(self, id):
        #ToDo
        pass

    @marshal_with(cart_args)
    def delete(self, id):
        #ToDo
        pass

    @marshal_with(cart_args)
    def put(self, id):
        #ToDo
        pass

class Carts(Resource):
    @marshal_with(cart_args)
    def get(self):
        carts = CartsModel.query.all()
        return carts

    @marshal_with(cart_args)
    def post(self):
        args = cart_args.parse_args()
        cart = CartsModel(productList=[], lastUpdate=dt.now(), createTime=dt.now(), owner=args['owner'])
        db.session.add(cart)
        db.session.commit()
        carts = CartsModel.query.all()
        return carts, 201


