from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from  flask_login import  LoginManager

app = Flask(__name__)
app.secret_key = "askhdaskdoai"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Myhoa_2399@localhost/bookdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="BOOK MANAGEMENT", template_mode= "bootstrap3")
login = LoginManager(app=app)