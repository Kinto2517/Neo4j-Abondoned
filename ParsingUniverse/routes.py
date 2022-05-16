import os
import secrets
from io import BytesIO

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, send_file
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from ParsingUniverse import app, db, bcrypt, uzanti_kontrol
from ParsingUniverse.forms import RegistrationForm, LoginForm, UpdateAccountForm, AdminLoginForm
from ParsingUniverse.models import User, PDFFile, Sorgu


@app.route('/aramaSorgu')
@login_required
def aramaSorgu():
    if current_user.is_authenticated:
        sorgular = Sorgu.query
        alldata = Sorgu.query.all()
        pdfdata = PDFFile.query.all()
        a = []
        b = []
        c = []
        for i in range(len(alldata)):
            a = Sorgu.query.filter_by(pdf_id=PDFFile.id).first()
            b = PDFFile.query.filter_by(id=a.pdf_id).first()
            c = b.user_username
    return render_template('aramaSorgu.html', title='Sorgu ',
                           sorgular=sorgular, pdfdata= c)

@app.route("/homeadmin")
@login_required
def homeadmin():
    if current_user.is_authenticated and current_user.is_admin():
        alldata = Sorgu.query.all()
        return render_template('homeadmin.html', alldata=alldata)
    else:
        return render_template('about.html')


@app.route("/home")
@login_required
def home():
    if current_user.is_authenticated:
        alldata = Sorgu.query.all()
        pdfdata = PDFFile.query.all()
        a=[]
        b=[]
        c=[]
        for i in range(len(alldata)):
                a = Sorgu.query.filter_by(pdf_id=PDFFile.id).first()
                b=  PDFFile.query.filter_by(id= a.pdf_id).first()
                c= b.user_username
        return render_template('home.html', alldata=alldata, pdfdata=c)
    else:
        return render_template('about.html')


@app.route('/sorguyap')
def sorguyap():
    return render_template("about.html")


@app.route('/dosyayukle', methods=['POST'])
@login_required
def dosyayukle():
    if request.method == 'POST':

        if 'dosya' not in request.files:
            flash('Dosya seçilmedi')
            return redirect('dosyayukleme')

        dosya = request.files['dosya']
        if dosya.filename == '':
            flash('Dosya seçilmedi')
            return redirect('dosyayukleme')

        if dosya and uzanti_kontrol(dosya.filename):
            dosyaadi = secure_filename(dosya.filename)

            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
            yenid = PDFFile(name=dosya.filename, user_username=current_user.username, data=dosya.read())
            db.session.add(yenid)
            db.session.commit()

            return redirect('dosyayukleme/' + dosyaadi)
        else:
            flash('İzin verilmeyen dosya uzantısı')
            return redirect('dosyayukleme')

    else:
        abort(401)


@app.route('/dosyayukleme')
@login_required
def dosyayukleme():
    return render_template("dosyayukleme.html")


@app.route('/dosyayukleme/<string:dosya>')
@login_required
def dosyayuklemesonuc(dosya):
    # response = requests.get()
    # text = extract_text(io.BytesIO(response.content))
    # print(text)
    return render_template("dosyayukleme.html")

@app.route("/")
@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route('/dosyaindirme/<string:dosya>')
@login_required
def dosyaindirme(dosya):
    dosya_data = PDFFile.query.filter_by(name=dosya).first()
    return send_file(BytesIO(dosya_data.data), attachment_filename='{}'.format(dosya), as_attachment=True)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.username.data == 'admin':
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, admin=1)
            db.session.add(user)
            db.session.commit()

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


    def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn


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


@app.route('/index')
@login_required
def index():
    if current_user.is_admin():
        alldata = User.query.all()
        return render_template('index.html', alldata=alldata)
    else:
        return render_template('about.html')


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    alldata = User.query.get(id)
    db.session.delete(alldata)
    db.session.commit()
    flash("Deleted")
    return redirect(url_for('index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        mydata = User.query.get(request.form.get('id'))
        mydata.username = request.form['username']
        mydata.email = request.form['email']
        a = request.form['password']
        hw = bcrypt.generate_password_hash(a).decode("utf-8")
        mydata.password = hw
        db.session.commit()
        flash("Updated Successfully")
        return redirect(url_for('index'))


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mydata = User(username=username, email=email, password=hashed_password)
        db.session.add(mydata)
        db.session.commit()
        flash("Added Successfully")
        return redirect(url_for('index'))

@app.route('/adminPdf', methods=['GET','POST'])
@login_required
def adminPdf():
    if current_user.is_admin():
        alldata = PDFFile.query.all()
        return render_template('adminPdf.html', alldata=alldata)
    else:
        return render_template('home.html')

@app.route('/kullaniciPdf', methods=['GET','POST'])
@login_required
def kullaniciPdf():
    if current_user.is_authenticated:
        alldata = PDFFile.query.all()
        return render_template('kullaniciPdf.html', alldata=alldata)
    else:
        return render_template('home.html')


