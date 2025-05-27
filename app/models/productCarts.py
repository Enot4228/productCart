from app import db

class CartsModel(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    productList = db.Column(db.String, nullable=True)
    lastUpdate = db.Column(db.DateTime, nullable=True)
    createTime = db.Column(db.DateTime, nullable=True)
    owner = db.Column(db.String, nullable=True, unique=True)
    isPaid = db.Column(db.Boolean, nullable=False, default=False)
