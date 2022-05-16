from datetime import datetime

from Researchers import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#
# class PDFFile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300))
#     user_username = db.Column(db.String(20), db.ForeignKey('user.username'), nullable=False)
#     date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     data = db.Column(db.LargeBinary)
# class Sorgu(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ad = db.Column(db.String(300), nullable=False)
#     soyad = db.Column(db.String(300), nullable=False)
#     ogrNo = db.Column(db.String(300), nullable=False)
#     ogrTur = db.Column(db.String(300), nullable=False)
#     dersAdi = db.Column(db.String(300), nullable=False)
#     donem = db.Column(db.String(300), nullable=False)
#     baslik = db.Column(db.String(300), nullable=False)
#     keyword = db.Column(db.String(300), nullable=False)
#     danisman = db.Column(db.String(300), nullable=False)
#     juri = db.Column(db.String(300), nullable=False)
#     ozet = db.Column(db.String(500), nullable=False)
#
#     pdf_id = db.Column(db.String(20), db.ForeignKey('pdf_file.id'), nullable=False)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, unique=False, default=False)

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

