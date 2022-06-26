from flask import Flask
from flask_login.utils import login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# import os
app = Flask(__name__)

# pic_folder = os.path.join('static','img')

#adding more configuration to app object so that it will recognize its database.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db' #adding key-value pair in config dictonary.
app.config['SECRET_KEY'] = 'dade92a7fe04b10b87113130'
# app.config['UPLOAD_FOLDER'] = pic_folder

# register_logo = os.path.join(app.config["UPLOAD_FOLDER"],"eagle_logo.png")
db = SQLAlchemy(app )
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
from market import routes
