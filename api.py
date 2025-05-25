from flask import Flask
from flask_restful import Api
from urls.routes import Carts


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/postgres"
api = Api(app)

#api.add_resource(urls.route.Cart, "/api/carts/<int:id>")
api.add_resource(Carts, "/api/carts/")
@app.route('/')
def home():
    return "<h1>Product Cart API</h1>"

if __name__ == '__main__':
    app.run(debug=True)