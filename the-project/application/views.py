# views.py
import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort, session
from application import app, db

from application.forms import UserRegistrationForm, UserLoginForm, AdoptionAddForm, ProductAddForm, UpdateAccountForm, MeetingAddForm, UpdateAccountFormUsername, UpdateAccountFormEmail, UpdateAccountFormPicture
from application.models import Pet, User, Product, PetRequest, Meeting
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, current_user, logout_user, login_required


admin = Admin(app)
## ADMIN VIEWS ####


class adminModelView(ModelView):
    pass


admin.add_view(adminModelView(Pet, db.session))
admin.add_view(adminModelView(User, db.session))
admin.add_view(adminModelView(Product, db.session))
admin.add_view(adminModelView(PetRequest, db.session))
admin.add_view(adminModelView(Meeting, db.session))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.route('/')
@app.route('/home')
def home():
    # return render_template('home.html',posts=post)
    return render_template('home.html', title="Home")


@app.route('/about')
@login_required
def about():
    return render_template('about.html', title="About")


@app.route('/adopt/<petType>', methods=['GET', 'POST'])
def adopt(petType):
    pets = Pet.query.filter_by(petType=petType).all()
    return render_template('petTable.html', title=petType, pets=pets, pettype=petType)


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    products = Product.query.all()
    productAnimalList = db.session.query(Product.productType).distinct()
    return render_template('shop.html', title='Shop', products=products, productAnimalList=productAnimalList)


@app.route('/shop/<productID>', methods=['GET', 'POST'])
def add(productID):
    if bool(Product.query.filter_by(id=productID).first()):
        product = Product.query.filter_by(id=productID).first()
        return render_template('productInfo.html', title='Product Info', product=product)
    else:
        abort(404)


@app.route("/petAdd/<petID>")
def adoptInfo(petID):
    if bool(Pet.query.filter_by(id=petID).first()):
        pet = Pet.query.filter_by(id=petID).first()
        return render_template('adoptInfo.html', title='Pet Info', pet=pet)
    else:
        abort(404)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(), firstName=form.firstName.data.capitalize(), lastName=form.lastName.data.capitalize(),
                    phone=form.phone.data, email=form.email.data.lower(), password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        # put in layout template that the flash messages show
        flash(f'Account created for {form.firstName.data} {form.lastName.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # show Austin how to debug (form.data.password)
        if user and (user.password == form.password.data):
            login_user(user)
            # put in layout template that the flash messages show
            flash(f'Logged in {user.firstName} {user.lastName}!', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)


def save_pictureUser(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pictureUser(form.picture.data)
            current_user.userPic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account information was updated successfully!', 'success')
        return redirect(url_for('myaccount'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('myAccount.html', title='My Account', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/animal_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/adoptionAdd", methods=['GET', 'POST'])
def adoptionAdd():
    form = AdoptionAddForm()
    if(current_user.is_authenticated):
        if form.validate_on_submit():
            picture_file = save_picture(form.picture.data)
            pet = PetRequest(petName=form.name.data, petType=dict(form.type.choices).get(form.type.data), petGender=dict(form.gender.choices).get(form.gender.data), petBreed=form.breed.data, petAge=form.age.data, petWeight=form.weight.data,
                             petContactFirstName=form.contactFirstName.data, petContactLastName=form.contactLastName.data, petContactEmail=form.contactEmail.data, petContactPhone=form.contactPhone.data, petImage=picture_file)
            db.session.add(pet)
            db.session.commit()
            flash(f'Application Has Been Sent for {form.name.data}!', 'success')
            return redirect(url_for('adoptionAdd'))
        elif request.method == 'GET':
            form.contactFirstName.data = current_user.firstName
            form.contactLastName.data = current_user.lastName
            form.contactEmail.data = current_user.email
            form.contactPhone.data = current_user.phone
        return render_template('adoptionAdd.html', title='Add Pet', form=form)

    else:
        return render_template('requestLogin.html', title="Please Log In")

@app.route("/meetingAdd", methods=['GET', 'POST'])
def meetingAdd():
    if(current_user.is_authenticated):
        form = MeetingAddForm()
        meetings = Meeting.query.all()
        if form.validate_on_submit() and form.submit.data:
            meeting = Meeting(meetingFirstName=current_user.firstName, meetingLastName=current_user.lastName,meetingDate=form.date.data, meetingEmail=current_user.email, meetingPhone=current_user.phone)
            db.session.add(meeting)
            db.session.commit()
            return render_template('confirm.html')
        return render_template('meetingAdd.html', title='Set Up A Meeting', form=form, meetings=meetings)
    else:
        return render_template('requestLogin.html', title="Please Log In")
