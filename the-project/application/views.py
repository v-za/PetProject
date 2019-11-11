# views.py
import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort, session
from application import app, db,login_manager,bcrypt

from application.forms import UserRegistrationForm, UserLoginForm, AdoptionAddForm, ProductAddForm, UpdateAccountForm, ApproveForm, DeclineForm
from application.forms import MeetingAddForm, UpdateAccountFormUsername, UpdateAccountFormEmail, UpdateAccountFormPicture
from application.models import Pet, User, Product, PetRequest, Meeting
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps


## ADMIN VIEWS ####


# decorators

# login role decorator

def login_required(role="open"):
    def wrapped(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
              return login_manager.unauthorized()
            if ((current_user.userRole != role) and (role != "open")):
                return login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapped


class adminHomeView(AdminIndexView):

    def is_accessible(self):

        if current_user.is_authenticated and current_user.userRole=="admin":
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('myaccount'))
        else:
            return redirect(url_for('login'))



class adminModelView(ModelView):

    create_modal = True
    edit_modal = True


    def is_accessible(self):

        if current_user.is_authenticated and current_user.userRole=="admin":
            return True
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('myaccount'))
        else:
            return redirect(url_for('login'))



admin = Admin(app,index_view = adminHomeView())
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
def about():
    return render_template('about.html', title="About")


@app.route('/adopt/<petType>', methods=['GET', 'POST'])
def adopt(petType):
    pets = Pet.query.filter_by(petType=petType).all()
    return render_template('petTable.html', title=petType, pets=pets, pettype=petType)


@app.route('/pets', methods=['GET', 'POST'])

def pets():
    pets = Pet.query.all()
    list = []
    if request.method == "POST":
        list = request.form.getlist("Animal")
        pets = Pet.query.filter(Pet.petType.in_(list)).all()
    return render_template('allPets.html', title="Pets", pets=pets)


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
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), firstName=form.firstName.data.capitalize(), lastName=form.lastName.data.capitalize(),
                    phone=form.phone.data, email=form.email.data.lower(), password=hash_password)
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
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
    if(current_user.is_authenticated):
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
    else:
        return render_template('requestLogin.html', title="Please Log In")


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/animal_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

def save_document(form_document):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_document.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/document_files', picture_fn)
    form_document.save(picture_path)
    return picture_fn

@app.route("/adoptionAdd", methods=['GET', 'POST'])
def adoptionAdd():
    form = AdoptionAddForm()
    if(current_user.is_authenticated):
        if form.validate_on_submit():
            picture_file = save_picture(form.picture.data)
            document_file = save_document(form.document.data)
            pet = PetRequest(petName=form.name.data, petType=dict(form.type.choices).get(form.type.data),
			                 petGender=dict(form.gender.choices).get(form.gender.data), petBreed=form.breed.data, petAge=form.age.data,
			                 petWeight=form.weight.data, petContactFirstName=form.contactFirstName.data, petContactLastName=form.contactLastName.data,
			                 petContactEmail=form.contactEmail.data, petContactPhone=form.contactPhone.data, petImage=picture_file, petDocument=document_file)
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
            meeting = Meeting(meetingFirstName=current_user.firstName, meetingLastName=current_user.lastName,meetingDate=form.date.data,
			                  meetingEmail=current_user.email, meetingPhone=current_user.phone)
            db.session.add(meeting)
            db.session.commit()
            return render_template('confirm.html')
        return render_template('meetingAdd.html', title='Set Up A Meeting', form=form, meetings=meetings)
    else:
        return render_template('requestLogin.html', title="Please Log In")

@app.route("/applications", methods=['GET', 'POST'])
def applications():
    if(current_user.is_authenticated and current_user.userRole == 'admin'):
        approve = ApproveForm()
        decline = DeclineForm()
        pets = PetRequest.query.all()
        if decline.validate_on_submit():
            obj = PetRequest.query.filter_by(id=pets.id).all()
            db.session.delete(obj)
            db.session.commit()
        return render_template('applications.html', title='Approve/Disapprove Apps', pets=pets, approve=approve, decline=decline)
    else:
        return render_template('requestLogin.html', title="Please Log In")

@app.route("/applications/<petID>/<method>", methods=['GET', 'POST'])
def applicationsID(petID,method):
    if(current_user.is_authenticated and current_user.userRole == 'admin'):
        if method == 'decline':
            pet = PetRequest.query.filter_by(id=petID).one()
            db.session.delete(pet)
            db.session.commit()
            flash(f'Application for {pet.petName} has been declined.', 'danger')
        elif method == 'approve':
            petR = PetRequest.query.filter_by(id=petID).one()
            pet = Pet(petName = petR.petName, petType=petR.petType, petGender=petR.petGender, petBreed=petR.petBreed, petAge = petR.petAge, petWeight=petR.petWeight, petImage = petR.petImage)
            db.session.add(pet)
            db.session.delete(petR)
            db.session.commit()
            flash(f'Application for {petR.petName} has been approved!', 'success')
        return redirect('/applications')
    else:
        return render_template('requestLogin.html', title="Please Log In")
