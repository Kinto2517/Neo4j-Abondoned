from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from Researchers import app, db, bcrypt
from Researchers.forms import RegistrationForm, LoginForm, UpdateAccountForm, AdminLoginForm
from Researchers.models import User


@app.route("/homeadmin")
@login_required
def homeadmin():

    return render_template('homeadmin.html')


@app.route("/home")
@login_required
def home():
    return render_template('home.html')


@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.username.data == 'admin' or form.username.data == 'derin':
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('adminlogin'))

        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and not user.is_admin():
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('about'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('homeadmin'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_admin():
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homeadmin'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('adminlogin.html', title='Admin Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('about'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

#
# @app.route('/delete/<id>/', methods=['GET', 'POST'])
# def delete(id):
#     alldata = User.query.get(id)
#     db.session.delete(alldata)
#     db.session.commit()
#     flash("Deleted")
#     return redirect(url_for('index'))
#
#
# @app.route('/update', methods=['GET', 'POST'])
# def update():
#     if request.method == 'POST':
#         mydata = User.query.get(request.form.get('id'))
#         mydata.username = request.form['username']
#         mydata.email = request.form['email']
#         a = request.form['password']
#         hw = bcrypt.generate_password_hash(a).decode("utf-8")
#         mydata.password = hw
#         db.session.commit()
#         flash("Updated Successfully")
#         return redirect(url_for('index'))
#
#
# @app.route('/insert', methods=['POST'])
# def insert():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         mydata = User(username=username, email=email, password=hashed_password)
#         db.session.add(mydata)
#         db.session.commit()
#         flash("Added Successfully")
#         return redirect(url_for('index'))
#
