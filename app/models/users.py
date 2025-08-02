from app import db, bcrypt

class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    hashedPassword = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

def create_user(args):
    return UsersModel(username=args['username'],
                      email=args['email'],
                      firstName=args['firstName'],
                      lastName=args['lastName'],
                      hashedPassword=bcrypt.generate_password_hash(args['password']).decode('utf-8'),
                      role=args['role'])
