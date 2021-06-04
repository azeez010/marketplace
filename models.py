from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from datetime import datetime
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)




app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://azeez:azeez007@localhost/bot'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dataslid:azeez007@dataslid.mysql.pythonanywhere-services.com/dataslid$betbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SECRET_KEY'] = "d27e0926-13d9-11eb-900d-18f46ae7891e"
app.config['TOKEN_EXPIRY_TIME'] = "10"


db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model, UserMixin ):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    is_admin = db.Column(db.Boolean, default=False)
    is_merchant = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(200))
    password = db.Column(db.String(150))
    merchant_wallet = db.Column(db.Integer, default=0)
    Referral_wallet = db.Column(db.Integer, default=0)
    account_number = db.Column(db.String(10))
    account_name = db.Column(db.String(100))
    account_bank = db.Column(db.String(40))


class Transaction_Table(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    ref_no = db.Column(db.String(50))
    amount = db.Column(db.String(15))
    # For recurring charges
    auth_code = db.Column(db.String(30))
    email = db.Column(db.String(30))
    cus_code = db.Column(db.String(30))
    paid_at = db.Column(db.String(80))
    product_data = db.Column(db.Text)
    transaction_complete = db.Column(db.Boolean, default=False)
    

class Bet_49ja(db.Model):
    __tablename__ = "bet_49ja"
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref=db.backref('bet_49ja', uselist=False), lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    is_building = db.Column(db.Boolean, default=False)
    has_compiled = db.Column(db.Boolean, default=False)
    bet9ja_username = db.Column(db.String(200))
    is_demo  = db.Column(db.Boolean, default=True)
    is_paid_bot = db.Column(db.Boolean, default=False)
    bot_type = db.Column(db.String(200), default="demo")
    bot_path = db.Column(db.String(2000))
    bot_mimetype = db.Column(db.String(200))
    is_subscribe = db.Column(db.Boolean, default=False)
    sub_exp_date = db.Column(db.String(500), default="0")

class Make_request(db.Model):
    __tablename__ = "make_request"
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='make_request', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    request = db.Column(db.Text)
    not_seen = db.Column(db.Boolean, default=True)
    datetime = db.Column(db.DateTime, default=datetime.now())

class Testimonial(db.Model):
    __tablename__ = "testimonial"
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='testimonial', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    testimony = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.now())

class Reset_password(db.Model):
    __tablename__ = 'reset_password'
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='reset_password', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    mail = db.Column(db.String(100))
    dateTime = db.Column(db.String(500), default=0)
    token = db.Column(db.String(150))
    
class Confirm_mail(db.Model):
    __tablename__ = 'confirm_mail'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100))
    user_details = db.Column(db.String(500))
    dateTime = db.Column(db.Integer)
    dateTime = db.Column(db.String(500), default=0)
    token = db.Column(db.String(150))

class Buy_pin(db.Model):
    __tablename__ = 'buy_pin'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(150))
    datetime = db.Column(db.DateTime, default=datetime.now())
    
class Subcribe_pin(db.Model):
    __tablename__ = 'subscribe_pin'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(150))
    datetime = db.Column(db.DateTime, default=datetime.now())
    

class Financial_data(db.Model):
    __tablename__ = 'financial_data'
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='financial_data', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    datetime = db.Column(db.DateTime, default=datetime.now())
    price = db.Column(db.String(15))
    bot_type = db.Column(db.String(60))


class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='store', lazy=True)
    store_name = db.Column(db.String(300))
    store_description = db.Column(db.Text)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    datetime = db.Column(db.DateTime, default=datetime.now())
    store_banner_url = db.Column(db.String(1000))
    store_logo_url = db.Column(db.String(1000))
    
class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    old_price = db.Column(db.Integer)
    accept_affliate = db.Column(db.Boolean, default=False)
    affliate_commission = db.Column(db.Integer, default=0)
    store  = db.relationship(Store, backref='products', lazy=True)
    store_id = db.Column(db.Integer(), db.ForeignKey(Store.id))
    datetime = db.Column(db.DateTime, default=datetime.now())
    # Links

    youtube_link = db.Column(db.String(1000))
    download_link = db.Column(db.String(3000))
    demo_link = db.Column(db.String(3000))
    thumbnail = db.Column(db.String(2000)) 
    
    # S3 Keys 
    demo_key = db.Column(db.String(1000))
    thumbnail_key = db.Column(db.String(1000)) 
    download_key = db.Column(db.String(1000)) 
    s3_expiry_time = db.Column(db.Integer)
    

class ProductImage(db.Model):
    __tablename__ = 'product_image'
    id = db.Column(db.Integer, primary_key=True)
    product = db.relationship(Products, backref='product_image', lazy=True)
    product_id = db.Column(db.Integer(), db.ForeignKey(Products.id))
    image_url = db.Column(db.String(1000))


class UserProducts(db.Model):
    __tablename__ = 'userproducts'
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='userproducts', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    product = db.relationship(Products, backref='userproducts', lazy=True)
    product_id = db.Column(db.Integer(), db.ForeignKey(Products.id))

class Referral(db.Model):
    __tablename__ = 'referral'
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='referral', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    product = db.relationship(Products, backref='referral', lazy=True)
    product_id = db.Column(db.Integer(), db.ForeignKey(Products.id))
    
# class StoreStats(db.Models):
#     __tablename__ = 'store_stats'
#     id = db.Column(db.Integer, primary_key=True)
#     user  = db.relationship(User, backref='store', lazy=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    # stats = 
    # stat_date = 

class Predictions(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(30))
    prediction = db.Column(db.Text)

class Predictions_access(db.Model):
    __tablename__ = 'predictions_access'
    id = db.Column(db.Integer, primary_key=True)
    user  = db.relationship(User, backref='predictions_access', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    predictions = db.relationship(Predictions, backref='predictions_access', lazy=True)
    predictions_id = db.Column(db.Integer(), db.ForeignKey(Predictions.id))
    sub_date = db.Column(db.DateTime, default=datetime.now())
    access = db.Column(db.Boolean, default=True)
    

if __name__ == '__main__':
    manager.run()
