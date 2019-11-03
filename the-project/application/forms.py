from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#inherting FlaskForm class

class UserRegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired("Too short"),Length(min=2, max=40) ])          #other arguments are constraints
    email = StringField('Email',validators=[DataRequired(),Email()])
    phone = StringField('Phone Number',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(message="Please Enter a Password")])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')


class UserLoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])          #other arguments are constraints
    password = PasswordField('Password',validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class AdoptionAddForm(FlaskForm):
    name = StringField('What is the name of the pet you are rehoming? (required)',validators=[DataRequired()])          #other arguments are constraints
    type = StringField('What species of animal is your pet? (required)',validators=[DataRequired()])
    breed = StringField('Do you know the breed of your pet? If so, put it here.')
    gender = StringField('Is your pet male or female?')
    age = IntegerField('How old is your pet? (Please put an integer. If you are unsure, you can guess)')
    picture = FileField('Upload a pic of your pet', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Send Request')

class MeetingAddForm(FlaskForm):
    date = StringField('What date do you want to visit? Check the list below for dates already taken.', validators=[DataRequired()])
    submit = SubmitField('Submit')
