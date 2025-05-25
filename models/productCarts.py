from api import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class CartsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productList = db.Columns(db.Array, nullable=True)
    lastUpdate = db.Column(db.DateTime, nullable=True)
    createTime = db.Column(db.DateTime, nullable=True)
    owner = db.Column(db.String, nullable=True)
    isPaid = db.Column(db.Boolean, nullable=False, default=False)
