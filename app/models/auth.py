from app import db

class AuthModel(db.Model):
    __tablename__ = 'auth'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)