from BookStoreManager import db,admin
from sqlalchemy import Column, Integer,Boolean, String ,Date, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from  flask_login import UserMixin, current_user,logout_user
from  flask_admin import  BaseView, expose

from flask import  redirect
import enum
from datetime import datetime
# class usertype(db.Model):
#     __tablename__ = 'category'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50), nullable=False)


class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    active = Column(Boolean, default=True)
    birthday = Column(Date, nullable=True)
    address = Column(String(100), nullable=True)
    phone = Column(Integer, nullable=True)
    Position = Column(String(50),nullable=True)
    loginname = Column(String(50),nullable=True)
    password = Column(String(50), default= True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    start_word_date = Column(Date)
    salary = Column(Float)


    def __str__ (self):
        return self.name
    # userType = Column(Integer, ForeignKey(usertype.id), nullable=False)
    #
    # def __str__(self):
    #     return self.hoten

# db.create_all()







class Customers(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable= False)
    birthday = Column(Date)
    address = Column(String(100))
    phone = Column(Integer)
    owe = Column(Float)

    def __str__ (self):
        return self.name



class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product',backref='category', lazy=True)

    def __str__ (self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    publisher = Column(String(100), nullable=True)
    publishing_year =Column(Integer)
    description = Column(String(500))
    amount = Column(Integer)
    update_date= Column(DateTime, default=datetime.now(),nullable=True)

    def __str__ (self):
        return self.name

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(Customers.id), primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now())
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    product_id = Column(Integer, ForeignKey(Product.id), primary_key=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)

class Report(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True)
    totalAmount = Column(Integer, default=0)
    totalOwe = Column(Integer, default=0)
    customer_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True)




class LougoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return  redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
# admin.add_view(LougoutView(name ="Log Out"))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Customers, db.session))
admin.add_view(ModelView(Receipt, db.session))
admin.add_view(ModelView(ReceiptDetail,db.session))
admin.add_view(LougoutView(name ="Log Out"))

db.create_all()