from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from application.models import User

#inherting FlaskForm class

class UserRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=40) ])
    firstName = StringField('First Name', validators=[DataRequired()])          #other arguments are constraints
    lastName = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(message="Please Enter a Password")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken. Please choose another one.")

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken. Please choose another one.")


class UserLoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])          #other arguments are constraints
    password = PasswordField('Password',validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AdoptionAddForm(FlaskForm):
    name = StringField('Pet Name',validators=[DataRequired()])          #other arguments are constraints
    type = StringField('Pet Type',validators=[DataRequired()])
    breed = StringField('Pet Breed',validators=[DataRequired()])
    gender = StringField('Pet Gender',validators=[DataRequired()])
    age = IntegerField('Pet Age',validators=[DataRequired()])
    weight = IntegerField('Pet Weight',validators=[DataRequired()])
    contactFirstName = StringField('Contact First Name',validators=[DataRequired()])
    contactLastName = StringField('Contact Last Name',validators=[DataRequired()])
    contactEmail = StringField('Contact Email',validators=[DataRequired(), Email()])
    contactPhone = StringField('Contact Phone',validators=[DataRequired()])
    #description = TextField('Pet Description', validators=[DataRequired()])
    picture = FileField('Profile Picture', validators=[DataRequired(), FileAllowed(['jpg','png'])])
    submit = SubmitField('Send Request')

class ProductAddForm(FlaskForm):
    productName = StringField('Product Name',validators=[DataRequired()])          #other arguments are constraints
    productType = StringField('Product Type',validators=[DataRequired()])
    productDesc = TextAreaField('Product Description',validators=[DataRequired()])
    productPrice = IntegerField('Product Price',validators=[DataRequired()])
    productInStock = IntegerField('Product Stock',validators=[DataRequired()])
    productImage = FileField('Product Picture', validators=[DataRequired(), FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Add Product')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2, max=40) ])
    email = StringField('Email',validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken. Please choose another one.")

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is taken. Please choose another one.")


class MeetingAddForm(FlaskForm):
    date = DateField('What date do you want to visit? (Check the list below to see what dates are already taken)',format='%Y-%m-%d',validators=[DataRequired()])
    submit = SubmitField('Submit')
