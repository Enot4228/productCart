from app import db

class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)