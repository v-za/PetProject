##from application import db
from application import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    phone = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}')"



class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petName = db.Column(db.String(20),nullable=False)
    petType = db.Column(db.String(20),nullable=False)
    petGender = db.Column(db.String(6),nullable=False)
    petBreed = db.Column(db.String(20),nullable=False)
    petAge = db.Column(db.Integer,nullable=False)
    petWeight = db.Column(db.Integer,nullable=False)
    petImage = db.Column(db.String(20), nullable=False, default='default.jpg')

#method for how our object is printed when printeed out
    def __repr__(self):
        return f"Pet('{self.petName}','{self.petType}','{self.petAge}', '{self.petImage}')"

class PetRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    petName = db.Column(db.String(20),nullable=False)
    petType = db.Column(db.String(20),nullable=False)
    petGender = db.Column(db.String(6))
    petBreed = db.Column(db.String(20))
    petAge = db.Column(db.Integer)
    petContactName = db.Column(db.String(80),nullable=False)
    petContactEmail = db.Column(db.String(80),nullable=False)
    petContactPhone = db.Column(db.String(80),nullable=False)
    petImage = db.Column(db.String(20), nullable=False, default='default.jpg')

#method for how our object is printed when printeed out
    def __repr__(self):
        return f"PetRequest('{self.petName}','{self.petType}','{self.petContact}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(40),nullable=False)
    productType = db.Column(db.String(20),nullable=False)
    productDesc = db.Column(db.String(400),nullable=False)
    productPrice = db.Column(db.Integer,nullable=False)
    productInStock = db.Column(db.Integer,nullable=False)
    #productImage =

#method for how our object is printed when printeed out
    def __repr__(self):
        return f"Product('{self.productName}','{self.productType}','{self.productAge}')"

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetingName = db.Column(db.String(40),nullable=False)
    meetingDate = db.Column(db.String(40),nullable=False)
    meetingEmail = db.Column(db.String(50),nullable=False)
    meetingPhone = db.Column(db.String(50),nullable=False)

db.create_all()
