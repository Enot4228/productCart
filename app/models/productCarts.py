from app import db

class CartsModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productList = db.Column(db.String, nullable=True)
    lastUpdate = db.Column(db.DateTime, nullable=True)
    createTime = db.Column(db.DateTime, nullable=True)
    owner = db.Column(db.String, nullable=True)
    isPaid = db.Column(db.Boolean, nullable=False, default=False)
