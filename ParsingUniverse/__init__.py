from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.utils import secure_filename

YUKLEME_KLASORU = 'ParsingUniverse/static/yuklemeler'
YUKLEME_KLASORU2 = 'ParsingUniverse/'

UZANTILAR = set(['pdf'])

def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU
app.config['UPLOAD_FOLDER2'] = YUKLEME_KLASORU2



db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from ParsingUniverse import routes

