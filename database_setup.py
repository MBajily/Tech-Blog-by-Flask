import os
import sys
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# Base = declarative_base()
db = SQLAlchemy(app)

#==============================================================
#                          Users
#==============================================================
class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(150))
    new_post = db.Column(db.String(30))
    edit_post = db.Column(db.String(30))
    delete_post = db.Column(db.String(30))
    new_phone_review = db.Column(db.String(30))
    edit_phone_review = db.Column(db.String(30))
    delete_phone_review = db.Column(db.String(30))
    new_laptop_review = db.Column(db.String(30))
    edit_laptop_review = db.Column(db.String(30))
    delete_laptop_review = db.Column(db.String(30))
    new_offer = db.Column(db.String(30))
    edit_offer = db.Column(db.String(30))
    delete_offer = db.Column(db.String(30))
    super_user = db.Column(db.String(30))

    def __repr__(self):
        return f"Users('{self.full_name}','{self.username}','{self.email}')"




#==============================================================
#                          Comments
#==============================================================

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    review_id = db.Column(db.Integer, ForeignKey('reviews.id'))
    review = db.relationship('Reviews', lazy=True)
    post_id = db.Column(db.Integer, ForeignKey('posts.id'))
    post = db.relationship('Posts', lazy=True)

    def __repr__(self):
        return f"Comments('{self.full_name}','{self.comment}','{self.publish_date}','{self.review_id}')"

    @property
    def serialize(self):
       
       return {
           'full_name'       : self.full_name,
           'comment'         : self.comment,
           'publish_date'    : self.publish_date,
        }

#==============================================================
#                          Replays
#==============================================================

class Replays(db.Model):
    __tablename__ = 'replays'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String(1000), nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    comment_id = db.Column(db.Integer, ForeignKey('comments.id'))
    comments = db.relationship('Comments', lazy=True)

    def __repr__(self):
        return f"Replays('{self.full_name}','{self.comment}','{self.publish_date}','{self.comment_id}')"

    @property
    def serialize(self):
       
       return {
           'full_name'       : self.full_name,
           'comment'         : self.comment,
           'publish_date'    : self.publish_date,
        }

    

#==============================================================
#                          Emails
#==============================================================

class Emails(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)



#==============================================================
#                          Brands
#==============================================================
class Brands(db.Model):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    name_ar = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(100))
    cover = db.Column(db.String(100))

    def __repr__(self):
        return f"Brands('{self.name}','{self.image}','{self.cover}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'name'         : self.name,
           'image'         : self.image,
        }


#==============================================================
#                          Categories
#==============================================================
class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(50), unique=True)
    name_ar = db.Column(db.String(50), unique=True)
    image = db.Column(db.String(100))

    def __repr__(self):
        return f"Categories('{self.name}','{self.image}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'name'         : self.name,
           'image'         : self.image,
        }


#==============================================================
#                           Markets
#==============================================================
class Markets(db.Model):
    __tablename__ = 'markets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    logo = db.Column(db.String(100))
    cover = db.Column(db.String(100))
    square = db.Column(db.String(100))

    def __repr__(self):
        return f"Markets('{self.name}','{self.logo}','{self.square}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'name'         : self.name
       }


#==============================================================
#                         Reviews
#==============================================================
class Reviews(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    name_ar = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(1000))
    content = db.Column(db.String(1000))
    image = db.Column(db.String(40))
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    brand_id = db.Column(db.Integer, ForeignKey('brands.id'), nullable=False)
    category = db.relationship('Categories', lazy=True) 
    brand = db.relationship('Brands', lazy=True)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    author = db.relationship('Users', lazy=True)

    def __repr__(self):
        return f"Reviews('{self.name}','{self.description}','{self.image}','{self.category}', '{self.brand}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'name'         : self.name,
           'description'         : self.description,
           'image'         : self.image,
       }


#==============================================================
#                            Offers
#==============================================================
class Offers(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(40), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)
    brand_id = db.Column(db.Integer, ForeignKey('brands.id'), nullable=False)
    review_id = db.Column(db.Integer, ForeignKey('reviews.id'))
    market_id = db.Column(db.Integer, ForeignKey('markets.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(150), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    storage_space = db.Column(db.String(100), nullable=False)
    category = db.relationship('Categories', lazy=True) 
    brand = db.relationship('Brands', lazy=True) 
    review = db.relationship('Reviews', lazy=True) 
    market = db.relationship('Markets', lazy=True) 
    checked = db.Column(db.String(40))

    def __repr__(self):
        return f"Offers('{self.name}','{self.image}','{self.price}','{self.category}', '{self.brand}','{self.review}','{self.market}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'name'         : self.name,
           'description'         : self.description,
           'image'         : self.image,
           'price'         : self.price,
           'url'         : self.url
       }




class Colors(db.Model):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_ar = db.Column(db.String(100))


class Storage_Space(db.Model):
    __tablename__ = 'storage_space'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

#==============================================================
#                         Advantages
#==============================================================
class Advantages(db.Model):
    __tablename__ = 'advantages'

    id = db.Column(db.Integer, primary_key=True)
    advantage = db.Column(db.String(100))
    product_id = db.Column(db.Integer, ForeignKey('reviews.id'), nullable=True)
    review = db.relationship('Reviews', lazy=True) 

    def __repr__(self):
        return f"Advantages('{self.advantage}','{self.review}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'advantage'         : self.advantage
       }


#==============================================================
#                        Disadvantages
#==============================================================
class Disadvantages(db.Model):
    __tablename__ = 'disadvantages'

    id = db.Column(db.Integer, primary_key=True)
    disadvantage = db.Column(db.String(100))
    product_id = db.Column(db.Integer, ForeignKey('reviews.id'), nullable=True)
    review = db.relationship('Reviews', lazy=True) 

    def __repr__(self):
        return f"Disadvantages('{self.disadvantage}','{self.review}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'disadvantage'         : self.disadvantage
       }


class Post_Types(db.Model):
    __tablename__ = 'post_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    name_ar = db.Column(db.String(50), unique=True)
    background_color = db.Column(db.String(50))


#==============================================================
#                            Posts
#==============================================================
class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(1000))
    image = db.Column(db.String(500))
    description = db.Column(db.String(1000))
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    post_type_id = db.Column(db.Integer, ForeignKey('post_types.id'), nullable=True)
    post_type = db.relationship('Post_Types', lazy=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=True)
    author = db.relationship('Users', lazy=True)


    def __repr__(self):
        return f"Posts('{self.title}','{self.content}','{self.image}','{self.publish_date}')"

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'title'         : self.title,
           'content'         : self.content,
           'image'         : self.image,
           'publish_date'         : self.publish_date
       }


#==============================================================
#                       Currency Converter
#==============================================================
class Currency_Converter(db.Model):
    __tablename__ = 'currency_converter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    name_ar = db.Column(db.String(100))
    amount = db.Column(db.Float)
    abbreviated = db.Column(db.String(100), unique=True)



#==============================================================
#                       Compare Phones
#==============================================================
class Compare_Phones(db.Model):
    __tablename__ = 'compare_phones'

    id = db.Column(db.Integer, primary_key=True)
    screen_size = db.Column(db.String(100))
    screen_type = db.Column(db.String(100))
    screen_resolution = db.Column(db.String(100))
    internal_storage_space = db.Column(db.String(100))
    external_storage_space = db.Column(db.String(100))
    ram = db.Column(db.String(100))
    battery_size = db.Column(db.String(100))
    fast_charging = db.Column(db.String(100))
    wireless_charging = db.Column(db.String(100))
    thickness = db.Column(db.String(100))
    height = db.Column(db.String(100))
    width = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    colors = db.Column(db.String(100))
    ports = db.Column(db.String(100))
    number_cameras = db.Column(db.String(100))
    cameras_specifications = db.Column(db.String(100))
    processor = db.Column(db.String(100))
    methods_securing = db.Column(db.String(100))
    os = db.Column(db.String(100))
    wireless_connectivity = db.Column(db.String(100))
    accessories = db.Column(db.String(100))
    product_id = db.Column(db.Integer, ForeignKey('reviews.id'))
    review = db.relationship('Reviews', lazy=True)

    def __repr__(self):
        return f"Compare_Phones('{self.screen_size}','{self.screen_type}','{self.screen_resolution}'"

    @property
    def serialize(self):
       
       return {
        }



#==============================================================
#                       Compare Phones
#==============================================================
class Compare_Laptops(db.Model):
    __tablename__ = 'compare_laptops'

    id = db.Column(db.Integer, primary_key=True)
    screen_size = db.Column(db.String(100))
    screen_type = db.Column(db.String(100))
    screen_resolution = db.Column(db.String(100))
    storage_space = db.Column(db.String(100))
    hard_disk_type = db.Column(db.String(100))
    battery_life = db.Column(db.String(100))
    thickness = db.Column(db.String(100))
    weight = db.Column(db.String(100))
    colors = db.Column(db.String(100))
    ports = db.Column(db.String(100))
    camera_properties = db.Column(db.String(100))
    processor_type = db.Column(db.String(100))
    processor_speed = db.Column(db.String(100))
    ram = db.Column(db.String(100))
    graphics_processor = db.Column(db.String(100))
    security = db.Column(db.String(100))
    os = db.Column(db.String(100))
    wireless_connection = db.Column(db.String(100))
    price = db.Column(db.String(100))
    product_id = db.Column(db.Integer, ForeignKey('reviews.id'))
    review = db.relationship('Reviews', lazy=True)

    def __repr__(self):
        return f"Compare_Phones('{self.screen_size}','{self.screen_type}','{self.screen_resolution}','{self.storage_space}','{self.hard_disk_type}','{self.battery_life}','{self.thickness}','{self.weight}','{self.colors}','{self.ports}','{self.camera_properties}','{self.processor_type}','{self.processor_speed}','{self.ram}','{self.graphics_processor}','{self.security}','{self.os}','{self.wireless_connection}','{self.prices}')"

    @property
    def serialize(self):
       
       return {
        }


#==============================================================
#                           Engine
#==============================================================
# engine = create_engine('sqlite:///TechDataBase.db')

# Base.metadata.create_all(engine)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TechDataBase.db'
    app.config['SQLALCHEMY_CONNECT_ARGS'] = {'check_same_thread': False}
    app.config['SQLALCHEMY_ECHO'] =True
    app.config['SQLALCHEMY_POOL_PRE_PING'] =True



