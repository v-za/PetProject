##from application import db
from application import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40),nullable=False)
    firstName = db.Column(db.String(20),nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)
    userPic = db.Column(db.String(20), nullable=False, default='default.png')


    def __repr__(self):
        return f"User('{self.firstName}', '{self.secondName}', '{self.email}')"



class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petName = db.Column(db.String(20),nullable=False)
    petType = db.Column(db.String(20),nullable=False)
    petGender = db.Column(db.String(6),nullable=False)
    petBreed = db.Column(db.String(20),nullable=False)
    petAge = db.Column(db.Integer,nullable=False)
    petWeight = db.Column(db.Integer,nullable=False)
    petImage = db.Column(db.String(20), nullable=False)

#method for how our object is printed when printeed out
    def __repr__(self):
        return f"Pet('{self.petName}','{self.petType}','{self.petAge}', '{self.petImage}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(40),nullable=False)
    productType = db.Column(db.String(20),nullable=False)
    productDesc = db.Column(db.Text,nullable=False)
    productPrice = db.Column(db.Numeric(5,2),nullable=False)
    productInStock = db.Column(db.Integer,nullable=False)
    productImage = db.Column(db.String(20), nullable=False, default = 'default.jpg')

#method for how our object is printed when printeed out
    def __repr__(self):
        return f"Product('{self.productName}','{self.productType}')"

#db.drop_all()
db.create_all()
