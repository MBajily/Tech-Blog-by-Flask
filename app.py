import os
import secrets
import pathlib
import sqlite3
from flask import Flask, render_template, redirect, url_for, request, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user, logout_user, login_user
from sqlalchemy.sql.expression import func
from database_setup import Users, Reviews, Offers, Markets, Advantages, Disadvantages, Posts, Brands, Categories, app, db, Colors, Storage_Space, Currency_Converter, Comments, Replays, Emails, Compare_Phones, Compare_Laptops, Post_Types
# from flask_wtf import FlaskForm
# from wtforms import StringField, TextField, SubmitField
# from wtforms.validators import DataRequired, Length, Email
# from wtforms.widgets import TextArea
from flask_mail import Mail, Message
from pathlib import Path
from itsdangerous.url_safe import URLSafeSerializer, URLSafeTimedSerializer



#=================================================================
#                  Import Modules For Check Offers
#=================================================================
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
import xlsxwriter
#=================================================================
#                  Import Modules For Check Offers
#=================================================================

app.config['SECRET_KEY'] = 'f71061567fef460551f5cbdc76e36c7f'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'logamyyt@gmail.com',
    MAIL_PASSWORD = '@Logamy1000$&@Logamy'
    ))

mail = Mail(app)


bcrypt=Bcrypt()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'yes'
login_manager.login_message_category = 'info'

login_manager.session_protection = "strong"
login_serializer = URLSafeTimedSerializer(app.secret_key)


@login_manager.user_loader
def lead_user(user_id):
    return Users.query.get(int(user_id))


# engine = create_engine('sqlite:///TechDataBase.db', connect_args={'check_same_thread': False}, echo=True, pool_pre_ping=True)
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind = engine)
# session = DBSession()
#=================================================================
# all_categories = Categories.query.all()
# all_brands = Brands.query.all()
# all_post = Posts.query.all()
# all_reviews = Reviews.query.all()
# all_offers = Offers.query.all()
# all_markets = Markets.query.all()
# all_colors = Colors.query.all()
# all_storages = Storage_Space.query.all()
# number_articals = len(Posts.query.filter_by(post_type_id=2).all())
# number_news = len(Posts.query.filter_by(post_type_id=1).all())
# number_programming = len(Posts.query.filter_by(post_type_id=3).all())
# number_phones = len(Reviews.query.filter_by(category_id=1).all())
# number_laptops = len(Reviews.query.filter_by(category_id=3).all())
# #=================================================================



class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')



#=================================================================
#                           Save Pictures
#=================================================================

def save_review_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Reviews/%s' %  picture_fn)
    form_picture.save(picture_path)
    return picture_fn



def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Posts/%s' % picture_fn)
    form_picture.save(picture_path)

    return '%s' % picture_fn



# def save_post_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/Articles/%s' % picture_fn)
#     form_picture.save(picture_path)

#     return 'Articles/%s' % picture_fn


def save_brands_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Brands/%s' % picture_fn)
    form_picture.save(picture_path)

    return '%s' % picture_fn



# @app.route("/checkOffersNow/dgdnsgew3j5yt5tefw/", methods=['GET', 'POST'])
# @login_required
# def checkOffersSouqcom():
#     countUpdates = 0
#     countDeletes = 0
#     all_offers = Offers.query.filter(Offers.checked == '' and Offers.category_id==1).all()
#     for offer in all_offers:
#         url = offer.url
#         print('---', offer.id , '---')
#         r = requests.get(url)
#         print(url)
#         soup = BeautifulSoup(r.content, "html.parser")
#         itemPrice = soup.find('h3',{'class' : 'price is sk-clr1'})
#         if itemPrice is not None and offer.checked != 'True':
#             price = itemPrice.text.replace(',', '').replace('ريـال', '').replace(' ', '').replace('\n', '').replace('\t', '').replace('\xa0', '')

#             offer.price = price
#             offer.price = price
#             offer.checked = 'True'
#             db.session.add(offer)
#             db.session.commit()
#             print(offer.id, ' has been UPDATED!')
#             countUpdates += 1
#         elif itemPrice is None:
#             # db.session.delete(offer)
#             # db.session.commit()
#             offer.checked = 'DELETED'
#             print(offer.id, ' has been DELETED!')
#             countDeletes += 1
#     flash('Updates: %s' % countUpdates, 'success')
#     flash('Deletes: %s' % countDeletes, 'danger')
#     return redirect(url_for('checkOffers'))

@app.route("/addNewOffers/addNewOffersEBay/", methods=['GET', 'POST'])
@login_required
def addNewOffersEBay():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    all_reviews = Reviews.query.all()
    all_markets = Markets.query.all()

    if request.method == 'POST':
        asincodes = request.form['asinCodes']
        asinCodes = asincodes.split('\r\n')
        if asincodes is not None:
            for asincode in asinCodes:
                if asincode.replace(' ','')!='':
                    # url = 'https://www.amazon.sa/gp/product/%s/tag=logamy-21' % asincode
                    url = asincode
                    r = requests.get(url)
                    print(url)
                    soup = BeautifulSoup(r.content, "html.parser")
                    img=soup.find('img', {'class' : 'vi-image-gallery__image vi-image-gallery__image--absolute-center'})
                    name=soup.find('h1', {'id' : 'itemTitle'})
                    price=soup.find('span', {'id' : 'prcIsum_bidPrice'})
                    if img is not None:
                        img = img.get('src')
                    else:
                        img=soup.find('img', {'class' : 'img img500 vi-img-gallery-vertical-align '})
                        if img is not None:
                            img = img.get('src')
                        else:
                            img=soup.find('img', {'id' : 'icImg'})
                            if img is not None:
                                img = img.get('src')


                    if name is None:
                        name=soup.find('h1', {'class' : 'it-ttl'})
                        if name is None:
                            name=soup.find('h1', {'class' : 'product-title'})
                            if name is not None:
                                name = name.text.strip('\r\n').replace('Details','').replace(' about','').replace('\xa0','')
                        else:
                            name = name.text.strip('\r\n').replace('Details','').replace(' about','').replace('\xa0','')
                    else:
                        name = name.text.strip('\r\n').replace('Details','').replace('about','').replace('\xa0','')


                    if price is None:
                        price=soup.find('span', {'class' : 'notranslate'})
                        if price is None:
                            price=soup.find('h2', {'class' : 'display-price'})
                            if price is None:
                                price=soup.find('span', {'id' : 'prcIsum'})
                        price = price.text.split('to', 1)[0]
                        if price.replace(' ','') == '':
                            price = price.get('content')

                        if "AU" in price:
                            price = float(price.replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*0.653227*3.75

                        elif "GBP" in price:
                            price = float(price.replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*1.22455*3.75

                        elif "C" in price:
                            price = float(price.replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*0.717165*3.75

                        else:
                            price = float(price.replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*3.75
                    else:
                        if "AU" in price:
                            price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*0.653227*3.75

                        elif "GBP" in price:
                            price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*1.22455*3.75

                        elif "C" in price:
                            price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*0.717165*3.75

                        else:
                            price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('US','').replace('$','').replace('GBP',''))*3.75
                    newOffer = Offers(name=name, image=img, price=price, url=url, name_ar=name,
                                category_id=request.form.get('Category'), brand_id=request.form.get('Brand'),
                                market_id=request.form.get('Market'), review_id=request.form.get('Review'),
                                checked='')
                    db.session.add(newOffer)
                    db.session.commit()
        return redirect(url_for('offers'))
    else:
        return render_template('addNewOffersEBay.html', first_posts=first_posts,
                            Reviews=Reviews, Users=Users, second_posts=second_posts, third_posts=third_posts,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews, 
                            Post_Types=Post_Types, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            all_categories=all_categories, all_brands=all_brands,
                            all_colors=all_colors, all_storages=all_storages,
                            all_reviews=all_reviews, all_markets=all_markets,
                            Categories=Categories)

@app.route("/checkOffersNow/checkOffersEBay/", methods=['GET', 'POST'])
@login_required
def checkOffersEBay():
    countUpdates = 0
    countDeletes = 0
    countDeletesSimilar = 0
    all_offers = Offers.query.filter(Offers.checked=='' and Offers.market_id==3).all()
    for offer in all_offers:
        url = offer.url
        print('---', offer.id , '---')
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.content, "html.parser")
        img=soup.find('img', {'class' : 'vi-image-gallery__image vi-image-gallery__image--absolute-center'})
        name=soup.find('h1', {'class' : 'product-title'})
        price=soup.find('h2', {'class' : 'display-price'})
        soled=soup.find('div', {'class' : 'app-cvip-replacement-message app-cvip-replacement-message-review'})
        if img is not None:
            img = img.get('src')
        else:
            img=soup.find('img', {'class' : 'img img500 vi-img-gallery-vertical-align '})
            if img is not None:
                img = img.get('src')
            else:
                img=soup.find('img', {'id' : 'icImg'})
                if img is not None:
                    img = img.get('src')

        if soled is None:
            if img is not None:
                img = img.get('src')
                if name is None:
                    name=soup.find('h1', {'class' : 'vi-title__main'})
                    name = name.text.strip('\r\n')
                else:
                    name = name.text.strip('\r\n')
                if price is None:
                    price=soup.find('span', {'class' : 'vi-bin-primary-price__main-price'})
                    if "AU" in price:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*0.653227*3.75

                    elif "GBP" in price:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*1.22455*3.75

                    elif "C" in price:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*0.717165*3.75

                    else:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*3.75
                else:
                    if "AU" in price:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*0.653227*3.75

                    elif "GBP" in price:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*1.22455*3.75

                    elif "C" in price:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*0.717165*3.75

                    else:
                        price = float(price.text.split('to', 1)[0].replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))*3.75



                offer.image = img
                offer.price = price
                offer.name = name
                offer.name_ar = name
                offer.checked = 'True'
                db.session.add(offer)
                db.session.commit()
                print(offer.id, ' has been UPDATED!')
                countUpdates += 1
            elif img is None:
                db.session.delete(offer)
                db.session.commit()
                # offer.checked = 'DELETED 2'
                print(offer.id, ' has been DELETED "Not Found!"')
                countDeletes += 1
        else:
            # offer.checked = 'DELETED 1'
            db.session.delete(offer)
            db.session.commit()
            print(offer.id, ' has been DELETED "Similar"')
            countDeletesSimilar += 1
    flash('Updates: %s' % countUpdates, 'success')
    flash('Deletes "Not Found!": %s' % countDeletes, 'danger')
    flash('Deletes "Similar Offer": %s' % countDeletesSimilar, 'warning')
    return redirect(url_for('checkOffers'))

@app.route("/addNewOffers/addNewOffersAmazonUSA/", methods=['GET', 'POST'])
@login_required
def addNewOffersAmazonUSA():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    all_reviews = Reviews.query.all()
    all_markets = Markets.query.all()

    if request.method == 'POST':
        asincodes = request.form['asinCodes']
        asinCodes = asincodes.split('\r\n')
        if asincodes is not None:
            for asincode in asinCodes:
                if asincode.replace(' ','')!='':
                    # url = 'https://www.amazon.sa/gp/product/%s/tag=logamy-21' % asincode
                    url = asincode
                    r = requests.get(url)
                    print(url)
                    soup = BeautifulSoup(r.content, "html.parser")
                    img=soup.find('img', {'class' : 'mainImage'})
                    name=soup.find('span', {'class' : 'a-size-large qa-title-text'})
                    price=soup.find('span', {'id' : 'price_inside_buybox'})
                    if img is not None:
                        img = img.get('src')
                        print('================1===============')

                    if name is not None:
                        name = name.text.strip('\r\n')
                        print('================2===============')
                    else:
                        name=soup.find('span', {'class' : 'a-size-large product-title-word-break'})
                        if name is not None:
                            name = name.text.strip('\r\n')
                            print('================3===============')
                        else:
                            name=soup.find('span', {'id' : 'productTitle'})
                            if name is not None:
                                name = name.text.strip('\r\n')
                                print('================4===============')
                            else:
                                name=soup.find('span', {'id' : 'productTitle'})
                                if name is not None:
                                    name = name.text.strip('\r\n')
                                    print('================5===============')
                    if price is not None:
                        price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))*3.75
                        print('================6===============')
                    # else:
                    #     price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockSalePriceString'})
                    #     if price is not None:
                    #         price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                    #     else: 
                    #         price=soup.find('span', {'class' : 'a-color-price'})
                    #         price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                    newOffer = Offers(name=name, image=img, price=price, url=url, name_ar=name,
                                category_id=request.form.get('Category'), brand_id=request.form.get('Brand'),
                                market_id=request.form.get('Market'), review_id=request.form.get('Review'),
                                checked='')
                    db.session.add(newOffer)
                    db.session.commit()
        return redirect(url_for('offers'))
    else:
        return render_template('addNewOffersAmazonUSA.html', first_posts=first_posts,
                            Reviews=Reviews, Users=Users, second_posts=second_posts, third_posts=third_posts,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews, 
                            Post_Types=Post_Types, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            all_categories=all_categories, all_brands=all_brands,
                            all_colors=all_colors, all_storages=all_storages,
                            all_reviews=all_reviews, all_markets=all_markets,
                            Categories=Categories)

@app.route("/checkOffersNow/checkOffersAmazonUSA/", methods=['GET', 'POST'])
@login_required
def checkOffersAmazonUSA():
    countUpdates = 0
    countDeletes = 0
    countDeletesSimilar = 0
    all_offers = Offers.query.filter(Offers.checked=='' and Offers.market_id==3).all()
    for offer in all_offers:
        url = offer.url
        print('---', offer.id , '---')
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.content, "html.parser")
        img=soup.find('img', {'class' : 'a-dynamic-image a-stretch-vertical'})
        name=soup.find('span', {'class' : 'a-size-large'})
        price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockBuyingPriceString'})
        if img is not None:
            img = img.get('src')
        else:
            name = name.text.strip('\r\n')
        if price is None:
            price=soup.find('span', {'class' : 'vi-bin-primary-price__main-price'})
            price = float(price.text.split('to', 1).replace(' ريـال', '').replace(',','').replace('C','').replace(' ','').replace('AU','').replace('$','').replace('GBP',''))

            offer.image = img
            offer.price = price
            offer.name = name
            offer.name_ar = name
            offer.checked = 'True'
            db.session.add(offer)
            db.session.commit()
            print(offer.id, ' has been UPDATED!')
            countUpdates += 1
        elif img is None:
            db.session.delete(offer)
            db.session.commit()
            # offer.checked = 'DELETED 2'
            print(offer.id, ' has been DELETED "Not Found!"')
            countDeletes += 1

    flash('Updates: %s' % countUpdates, 'success')
    flash('Deletes "Not Found!": %s' % countDeletes, 'danger')
    flash('Deletes "Similar Offer": %s' % countDeletesSimilar, 'warning')
    return redirect(url_for('checkOffers'))

@app.route("/addNewOffers/addNewOffersAmazonSa/", methods=['GET', 'POST'])
@login_required
def addNewOffersAmazonSa():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    all_reviews = Reviews.query.all()
    all_markets = Markets.query.all()

    if request.method == 'POST':
        asincodes = request.form['asinCodes']
        asinCodes = asincodes.split('\r\n')
        if asincodes is not None:
            for asincode in asinCodes:
                if asincode.replace(' ','')!='':
                    # url = 'https://www.amazon.sa/gp/product/%s/tag=logamy-21' % asincode
                    url = asincode
                    r = requests.get(url)
                    print(url)
                    soup = BeautifulSoup(r.content, "html.parser")
                    img=soup.find('img', {'id' : 'landingImage'})
                    name=soup.find('span', {'id' : 'productTitle'})
                    price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockBuyingPriceString'})
                    if price is not None:
                        img = img.get('src')
                    else:
                        img=soup.find('img', {'class' : 'a-dynamic-image a-stretch-horizontal'})
                        img = img.get('src')

                    name = name.text.strip('\r\n')
                    if price is not None:
                        price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                    else:
                        price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockSalePriceString'})
                        if price is not None:
                            price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                        else: 
                            price=soup.find('span', {'class' : 'a-color-price'})
                            price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                    newOffer = Offers(name=name, image=img, price=price, url=url, name_ar=name,
                                category_id=request.form.get('Category'), brand_id=request.form.get('Brand'),
                                market_id=request.form.get('Market'), review_id=request.form.get('Review'),
                                checked='')
                    db.session.add(newOffer)
                    db.session.commit()
        return redirect(url_for('offers'))
    else:
        return render_template('addNewOffersAmazonSa.html', first_posts=first_posts,
                            Reviews=Reviews, Users=Users, second_posts=second_posts, third_posts=third_posts,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews, 
                            Post_Types=Post_Types, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            all_categories=all_categories, all_brands=all_brands,
                            all_colors=all_colors, all_storages=all_storages,
                            all_reviews=all_reviews, all_markets=all_markets,
                            Categories=Categories)

@app.route("/checkOffersNow/checkOffersAmazonSa/", methods=['GET', 'POST'])
@login_required
def checkOffersAmazonSa():
    countUpdates = 0
    countDeletes = 0
    countDeletesSimilar = 0
    all_offers = Offers.query.filter_by(market_id=1).filter_by(checked='').all()
    for offer in all_offers:
        url = offer.url
        print('---', offer.id , '---')
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.content, "html.parser")
        img=soup.find('img', {'id' : 'landingImage'})
        name=soup.find('span', {'id' : 'productTitle'})
        price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockBuyingPriceString'})
        if img is not None:
            name = name.text.strip('\r\n')
            img = img.get('src')
            if price is not None:
                
                    price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                    offer.price = price
            elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.':
                price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockSalePriceString'})
                if price is not None:
                    
                        price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                        offer.price = price
                elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                    price=soup.find('span', {'class' : 'a-color-price'})
                    
            offer.image = img
            offer.name = name
            offer.name_ar = name
            offer.checked = 'True'
            db.session.add(offer)
            db.session.commit()
            print(offer.id, ' has been UPDATED!')
            countUpdates += 1
        else:
            
            img=soup.find('img', {'class' : 'a-dynamic-image a-stretch-horizontal'})
            if img is not None:
                name = name.text.strip('\r\n')
                img = img.get('src')
                if price is not None:
                    
                        price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                        offer.price = price
                elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.':
                    price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockSalePriceString'})
                    if price is not None:
                        
                            price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                            offer.price = price
                    elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                        price=soup.find('span', {'class' : 'a-color-price'})
                        if price is not None:
                            
                                price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                                offer.price = price
                        elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                            price=soup.find('span', {'id' : 'priceblock_ourprice'})
                            if price is not None:
                                
                                    price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                                    offer.price = price
                            elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                                price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockBuyingPriceString'})
                offer.image = img
                offer.name = name
                offer.name_ar = name
                offer.checked = 'True'
                db.session.add(offer)
                db.session.commit()
                print(offer.id, ' has been UPDATED!')
                countUpdates += 1
            elif img is None:
                img=soup.find('img', {'class' : 'a-dynamic-image a-stretch-vertical'})
                if img is not None:
                    name = name.text.strip('\r\n')
                    img = img.get('src')
                    if price is not None:
                        price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                        offer.price = price
                    elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.':
                        price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockSalePriceString'})
                        if price is not None:
                            price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                            offer.price = price
                        elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                            price=soup.find('span', {'class' : 'a-color-price'})
                            if price is not None:
                                price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                                offer.price = price
                            elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                                price=soup.find('span', {'id' : 'priceblock_ourprice'})
                                if price is not None:
                                    price = float(price.text.replace(' ريـال', '').replace(',','').replace('\xa0','').replace(' ','').replace('ريال','').replace('$','').replace('GBP',''))
                                    offer.price = price
                                elif price is None or price.strip('\r\n') == 'غيرمتوفرحالياً.' or price.strip('\r\n') == 'غيرمتوفرحالياً.': 
                                    price=soup.find('span', {'class' : 'a-size-medium a-color-price priceBlockBuyingPriceString'})
                    offer.image = img
                    offer.name = name
                    offer.name_ar = name
                    offer.checked = 'True'
                    db.session.add(offer)
                    db.session.commit()
                    print(offer.id, ' has been UPDATED!')
                    countUpdates += 1

                elif img is None:
                    db.session.delete(offer)
                    db.session.commit()
                    # offer.checked = 'DELETED 2'
                    print(offer.id, ' has been DELETED "Not Found!"')
                    countDeletes += 1

        
        

    flash('Updates: %s' % countUpdates, 'success')
    flash('Deletes "Not Found!": %s' % countDeletes, 'danger')
    flash('Deletes "Similar Offer": %s' % countDeletesSimilar, 'warning')
    return redirect(url_for('checkOffers'))

#=================================================================
#                           Home Page
#=================================================================
# Here is  the route of the home page and it will contain :
#   1-navbar[]. 2-all categories[done]. 3-some brands[done]. 4-some post[done].
#   5-some reviews[done]. 6-random ads[].
@app.route("/")
@app.route("/home/")
def homepage():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #=======================================================
    brands = Brands.query.all()
    random_phone_offers = Offers.query.filter_by(category_id=1).order_by(func.random()).limit(8).all()
    random_laptop_offers = Offers.query.filter_by(category_id=3).order_by(func.random()).limit(5).all()
    random_brands = Brands.query.order_by(func.random()).limit(3).all()
    latest_posts = Posts.query.order_by(Posts.publish_date.desc()).limit(4).all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()    #==================================================================================
    bottom_reviews = Reviews.query.order_by(Reviews.publish_date.desc()).limit(8).all()
    random_posts = Posts.query.filter(Posts not in latest_posts).order_by(func.random()).limit(4).all()
    return render_template('homepage.html', title='الصفحة الرئيسية | لوجامي للتقنية',
                            pageDescription='في موقع لوجامي للتقنية سنقوم بتوفير مراجعة لكل ما هو جديد في عالم التكنولوجيا وبالاخص في مجال الهواتف المحمولة واللابتوبات. وسنوفر لك اسهل طريقة لمقارنة اسعار المنتجات التي ترغب بها عبر العديد من المتاجر الالكترونية. لكي نضمن لك الحصول على ما ترغب به باقل الاسعار وكل ذلك عبر صفحة العروض.',
                            keywords='في موقع لوجامي للتقنية سنقوم بتوفير مراجعة لكل ما هو جديد في عالم التكنولوجيا وبالاخص في مجال الهواتف المحمولة واللابتوبات. وسنوفر لك اسهل طريقة لمقارنة اسعار المنتجات التي ترغب بها عبر العديد من المتاجر الالكترونية. لكي نضمن لك الحصول على ما ترغب به باقل الاسعار وكل ذلك عبر صفحة العروض.'.replace(' ',', '),
                            all_categories=all_categories, brands=brands,
                            latest_posts=latest_posts, all_brands=all_brands,
                            Categories=Categories, Brands=Brands, len=len, int=int,
                            random_phone_offers=random_phone_offers,
                            random_laptop_offers=random_laptop_offers, format=format,
                            float=float, round=round, first_posts=first_posts,
                            Reviews=Reviews, Users=Users, second_posts=second_posts,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews, Markets=Markets,
                            Post_Types=Post_Types, random_brands=random_brands,
                            third_posts=third_posts, bottom_reviews=bottom_reviews,
                            random_posts=random_posts, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops)



#=================================================================
#                            About
#=================================================================
@app.route("/about/")
def about():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================

    return render_template('about.html', title='حولنا | لوجامي للتقنية',
                            pageDescription='في موقع لوجامي للتقنية سنقوم بتوفير مراجعة لكل ما هو جديد في عالم التكنولوجيا وبالاخص في مجال الهواتف المحمولة واللابتوبات. وسنوفر لك اسهل طريقة لمقارنة اسعار المنتجات التي ترغب بها عبر العديد من المتاجر الالكترونية. لكي نضمن لك الحصول على ما ترغب به باقل الاسعار وكل ذلك عبر صفحة العروض.',
                            keywords='في موقع لوجامي للتقنية سنقوم بتوفير مراجعة لكل ما هو جديد في عالم التكنولوجيا وبالاخص في مجال الهواتف المحمولة واللابتوبات. وسنوفر لك اسهل طريقة لمقارنة اسعار المنتجات التي ترغب بها عبر العديد من المتاجر الالكترونية. لكي نضمن لك الحصول على ما ترغب به باقل الاسعار وكل ذلك عبر صفحة العروض.'.replace(' ',', '),
                            all_categories=all_categories, all_brands=all_brands,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                            first_posts=first_posts, second_posts=second_posts,
                            third_posts=third_posts, Users=Users, Post_Types=Post_Types,
                            Categories=Categories, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops)


#=================================================================
#                            show Author
#=================================================================
@app.route("/authors/<int:author_id>/")
def showAuthor(author_id):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedAuthor = Users.query.filter_by(id=author_id).one()
    author_reviews = Reviews.query.filter_by(author_id=author_id).order_by(Reviews.publish_date.desc()).all()
    author_posts = Posts.query.filter_by(author_id=author_id).order_by(Posts.publish_date.desc()).all()
    author_number_reviews = len(author_reviews)
    author_number_posts = len(author_posts)
    return render_template('showAuthor.html', title='%s | لوجامي للتقنية' % selectedAuthor.full_name,
                            pageDescription=selectedAuthor.about,
                            keywords='%s, %s, %s' % ('لوجامي للتقنية, logamy technology', selectedAuthor.full_name, selectedAuthor.about.replace(' ', ', ')),
                            all_categories=all_categories, all_brands=all_brands,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                            first_posts=first_posts, second_posts=second_posts,
                            third_posts=third_posts, Users=Users, Post_Types=Post_Types,
                            Categories=Categories, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            selectedAuthor=selectedAuthor, author_reviews=author_reviews,
                            author_posts=author_posts, author_number_reviews=author_number_reviews,
                            author_number_posts=author_number_posts)


@app.route("/privacy_policy/")
def privacyPolicy():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    return render_template('Privacy_policy.html', title='سياسة الخصوصية | لوجامي للتقنية',
                            pageDescription='خصوصيتك أيها الزائر لها أهمية بالغة بالنسبة لنا ، و سياسة الخصوصية الموجودة في هذه الوثيقة تمثل الخطوط العريضة لأنواع المعلومات الشخصية التي موقع لوجامي للتقنية وكيفية استخدام هذه المعلومات.',
                            keywords='خصوصيتك أيها الزائر لها أهمية بالغة بالنسبة لنا ، و سياسة الخصوصية الموجودة في هذه الوثيقة تمثل الخطوط العريضة لأنواع المعلومات الشخصية التي موقع لوجامي للتقنية وكيفية استخدام هذه المعلومات.'.replace(' ', ', '),
                            all_categories=all_categories,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                            first_posts=first_posts, second_posts=second_posts,
                            third_posts=third_posts, Users=Users, Post_Types=Post_Types,
                            Categories=Categories, all_brands=all_brands, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops)
#=================================================================
#                         Contact Us
#=================================================================


@app.route("/contact/", methods=['GET', 'POST'])
def contact():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    if request.method == 'POST':
        mydict = {'message':request.form['message'],'contact_email':request.form['email']}
        result_dict = {}
        try:
            msg = Message('"'+ request.form['title'] + '" | ' + request.form['full_name'],sender=request.form['email'],recipients=["logamyyt@gmail.com"])
            msg.body = mydict['message'] + "\n\n" + request.form['email']
            mail.send(msg)
            flash('عزيزي {}. '.format(request.form['full_name']) + 'نشكرك على تواصلك معنا نعدك باننا سنقوم بالرد عليك باسرع وقت ممكن', 'success')
        except Exception as e:
            flash("Error sending email {}".format(str(e)) + 'error.', 'danger')


        return render_template("contact.html" ,title="اتصل بنا | لوجامي للتقنية",
                                pageDescription='اتصل بنا اذا كان لديك اي مشكلة او استفسار وسنقوم بالرد عليك في اسرع وقت ممكن',
                                keywords='اتصل بنا اذا كان لديك اي مشكلة او استفسار وسنقوم بالرد عليك في اسرع وقت ممكن'.replace(' ',', '),
                                phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                first_posts=first_posts, second_posts=second_posts,
                                third_posts=third_posts, Users=Users, Post_Types=Post_Types,
                                Categories=Categories, all_brands=all_brands, number_articals=number_articals,
                                number_news=number_news, number_programming=number_programming,
                                number_phones=number_phones, number_laptops=number_laptops)

    return render_template("contact.html",title="اتصل بنا | لوجامي للتقنية",
                                pageDescription='اتصل بنا اذا كان لديك اي مشكلة او استفسار وسنقوم بالرد عليك في اسرع وقت ممكن',
                                keywords='اتصل بنا اذا كان لديك اي مشكلة او استفسار وسنقوم بالرد عليك في اسرع وقت ممكن'.replace(' ',', '),
                                phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                first_posts=first_posts, second_posts=second_posts,
                                third_posts=third_posts, Users=Users, Post_Types=Post_Types,
                                Categories=Categories, all_brands=all_brands, number_articals=number_articals,
                                number_news=number_news, number_programming=number_programming,
                                number_phones=number_phones, number_laptops=number_laptops)



#=================================================================
#                             Login
#=================================================================
# Here is the rout of login page it will contain:
#   1-username[]. 2-password[]. 3-login button[].

@app.route("/login/", methods=['GET', 'POST'])
def login():   # script[done]      # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))

    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['Username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['Password']):
            login_user(user)
            message = "logged in successfully as {}".format(user.username)
            message_category = 'success'
            return redirect(url_for('homepage'))
        message = "Incorrect username or password"
        message_category = 'danger'
        return render_template("login.html", message=message, message_category=message_category,
                                phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                first_posts=first_posts, second_posts=second_posts,
                                third_posts=third_posts, number_articals=number_articals,
                                number_news=number_news, number_programming=number_programming,
                                number_phones=number_phones, number_laptops=number_laptops,
                                Categories=Categories, Users=Users, Post_Types=Post_Types)

    return render_template("login.html", phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                first_posts=first_posts, second_posts=second_posts,
                                third_posts=third_posts, number_articals=number_articals,
                                number_news=number_news, number_programming=number_programming,
                                number_phones=number_phones, number_laptops=number_laptops,
                                Categories=Categories, Users=Users, Post_Types=Post_Types)



@app.route('/logout/')
@login_required
def logout():   # script[done]
    logout_user()
    return redirect(url_for('homepage'))



#=================================================================
#                           Categories
#=================================================================


# @app.route("/3tg4h45u63w4hg4w5/", methods=['GET', 'POST'])
# def writeReviewComments():
#     if request.method=='POST':
#         review_id = request.form['Review']
#         review = Reviews.query.filter_by(id=review_id).one()
#         emails_list = []
#         all_emails = Emails.query.all()
#         for email in all_emails:
#             emails_list.append(email.email)
#         addComment = Comments(full_name=request.form['full_name'], email=request.form['email'], comment=request.form['comment'], review_id=review_id)

#         if request.form['email'] in emails_list:
#             deleteEmail = Emails.query.filter_by(email=request.form['email']).one()
#             db.session.delete(deleteEmail)
#             db.session.commit()
#             newEmail = Emails(full_name=request.form['full_name'], email=request.form['email'])
#             db.session.add(newEmail)
#         else:
#             newEmail = Emails(full_name=request.form['full_name'], email=request.form['email'])
#             db.session.add(newEmail)

#         db.session.add(addComment)

#         db.session.commit()

#         return redirect(url_for('showReview', review_id=review_id, review_url='مراجعة_%s' % review.name_ar.replace(' ','_')))


#     return redirect(url_for('homepage'))

@app.route("/mail_list/", methods=['GET', 'POST'])
def mailList():
    all_emails = Emails.query.all()
    email_list = []
    for email in all_emails:
        email_list.append(email.email)
    if request.method=='POST':
        if request.form['email']:
            if request.form['email'] in email_list:

                deleteEmail = Emails.query.filter_by(email=request.form['email']).one()
                Full_Name = deleteEmail.full_name
                db.session.delete(deleteEmail)
                db.session.commit()
                newEmail = Emails(full_name=Full_Name, email=request.form['email'])
                db.session.add(newEmail)
                db.session.commit()
            else:
                newEmail = Emails(email=request.form['email'])
                db.session.add(newEmail)
                db.session.commit()
        return redirect(url_for('homepage'))
    return redirect(url_for('homepage'))


@app.route("/posts/comments/write/", methods=['GET', 'POST'])
def writePostComments():
    if request.method=='POST':
        post_id = request.form['Review_ID']
        selectedPost = Reviews.query.filter_by(id=post_id).one()
        emails_list = []
        all_emails = Emails.query.all()
        for email in all_emails:
            emails_list.append(email.email)
        addComment = Comments(full_name=request.form['name'], email=request.form['email'], comment=request.form['message'], post_id=request.form['Post_ID'], review_id='')

        if request.form['email'] in emails_list:
            deleteEmail = Emails.query.filter_by(email=request.form['email']).one()
            db.session.delete(deleteEmail)
            db.session.commit()
            newEmail = Emails(full_name=request.form['name'], email=request.form['email'])
            db.session.add(newEmail)
        else:
            newEmail = Emails(full_name=request.form['name'], email=request.form['email'])
            db.session.add(newEmail)

        db.session.add(addComment)

        db.session.commit()

        return redirect(url_for('showPost', post_id=post_id, post_url='%s' % selectedPost.name.replace(' ','_')))


    return redirect(url_for('homepage'))


@app.route("/reviews/comments/write/", methods=['GET', 'POST'])
def writeReviewComments():
    if request.method=='POST':
        review_id = request.form['Review_ID']
        review = Reviews.query.filter_by(id=review_id).one()
        emails_list = []
        all_emails = Emails.query.all()
        for email in all_emails:
            emails_list.append(email.email)
        addComment = Comments(full_name=request.form['name'], email=request.form['email'], comment=request.form['message'], review_id=request.form['Review_ID'])

        if request.form['email'] in emails_list:
            deleteEmail = Emails.query.filter_by(email=request.form['email']).one()
            db.session.delete(deleteEmail)
            db.session.commit()
            newEmail = Emails(full_name=request.form['name'], email=request.form['email'])
            db.session.add(newEmail)
        else:
            newEmail = Emails(full_name=request.form['name'], email=request.form['email'])
            db.session.add(newEmail)

        db.session.add(addComment)

        db.session.commit()

        return redirect(url_for('showReview', review_id=review_id, review_url='%s_Review' % review.name.replace(' ','_')))


    return redirect(url_for('homepage'))

# @app.route("/review/<int:review_id>/comments", methods=['GET', 'POST'])
# def comments(review_id):
#     review = Reviews.query.filter_by(id=review_id).one()
#     all_comments = Comments.query.filter_by(review_id=review_id).order_by(Comments.publish_date).all()

#     return render_template("comments.html", title="جميع التعليقات | %s" % review.name_ar, all_comments=all_comments,
#                             review=review, len=len, Replays=Replays,
#                             all_categories=all_categories, all_brands=all_brands)



@app.route("/comment/<int:comment_id>/delete/", methods=['GET', 'POST'])
@login_required
def deleteComment(comment_id):    # script[done]    # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedComment = Comments.query.filter_by(id=comment_id).one()
    selectedReview = Reviews.query.filter_by(id=selectedComment.review_id).one()
    if request.method == 'POST':
        all_replays = Replays.query.filter_by(comment_id=selectedComment.id).all()
        for replay in all_replays:
            db.session.delete(replay)
            db.session.commit()
        db.session.delete(selectedComment)
        db.session.commit()
        flash('التعليق الخاص ب%s قد تم حذفه بنجاح.' % selectedComment.full_name, 'danger')
        return redirect(url_for('showReview', review_id=selectedReview.id, review_url='%s_Review' % selectedReview.name.replace(' ','_')))
    else:
        return render_template('deleteComment.html', title='حذف | %s' % selectedComment.full_name,
                                selectedComment=selectedComment,
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories,
                                selectedReview=selectedReview)


@app.route("/comments/<int:comment_id>/edit/", methods=['GET', 'POST'])
def editComment(comment_id):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedComment = Comments.query.filter_by(id=comment_id).one()
    selectedReview = Reviews.query.filter_by(id=selectedComment.review_id).one()
    if request.method == 'POST':
        if request.form['Full_name']:
            selectedComment.full_name = request.form['Full_name']
        if request.form['Comment']:
            selectedComment.comment = request.form['Comment']
        db.session.add(selectedComment)
        db.session.commit()
        flash('التعليق الخاص ب%s قد تم تعديله بنجاح.' % selectedComment.full_name, 'info')
        return redirect(url_for('showReview', review_id=selectedReview.id, review_url='%s_Review' % selectedReview.name.replace(' ','_')))
    else:
        return render_template('editComment.html', title='تعديل | %s' % selectedComment.full_name,
                                selectedComment=selectedComment, all_categories=all_categories,
                                all_brands=all_brands, Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories,
                                selectedReview=selectedReview)
#=================================================================
#                           replays
#=================================================================


@app.route("/replays/write/", methods=['GET', 'POST'])
def writeReplays():
    if request.method=='POST':
        comment_id = request.form['Comment']
        emails_list = []
        all_emails = Emails.query.all()
        for email in all_emails:
            emails_list.append(email.email)

        if request.form['email'] in emails_list:
            deleteEmail = Emails.query.filter_by(email=request.form['email']).one()
            db.session.delete(deleteEmail)
            db.session.commit()
            newEmail = Emails(full_name=request.form['name'], email=request.form['email'])
            db.session.add(newEmail)
            db.session.commit()
        else:
            newEmail = Emails(full_name=request.form['name'], email=request.form['email'])
            db.session.add(newEmail)
            db.session.commit()
        addReplay = Replays(full_name=request.form['name'], email=request.form['email'], comment=request.form['message'], comment_id=comment_id)
        db.session.add(addReplay)

        db.session.commit()
        return redirect(url_for('replays', comment_id=comment_id))

    return redirect(url_for('homepage'))


@app.route("/comment/<int:comment_id>/replays/", methods=['GET', 'POST'])
def replays(comment_id):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedComment = Comments.query.filter_by(id=comment_id).one()
    all_replays = Replays.query.filter_by(comment_id=selectedComment.id).order_by(Replays.publish_date).all()
    selectedReview = Reviews.query.filter_by(id=selectedComment.review_id).one()
    return render_template("replays.html", title="الردود | %s" % selectedComment.full_name,
                            pageDescription=selectedComment.comment,
                            keywords=selectedComment.comment.replace(' ', ', '),
                            all_replays=all_replays, selectedComment=selectedComment, len=len,
                            all_categories=all_categories, all_brands=all_brands,
                            Post_Types=Post_Types, phone_reviews=phone_reviews,
                            laptop_reviews=laptop_reviews, first_posts=first_posts,
                            second_posts=second_posts, third_posts=third_posts,
                            number_articals=number_articals, number_news=number_news,
                            number_programming=number_programming, number_phones=number_phones,
                            number_laptops=number_laptops, Users=Users, Categories=Categories,
                            selectedReview=selectedReview)



@app.route("/replays/<int:replay_id>/delete/", methods=['GET', 'POST'])
@login_required
def deleteReplay(replay_id):    # script[done]    # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedReplay = Replays.query.filter_by(id=replay_id).one()
    comment = Comments.query.filter_by(id=selectedReplay.comment_id).one()
    if request.method == 'POST':
        db.session.delete(selectedReplay)
        db.session.commit()
        flash('التعليق الخاص ب%s قد تم حذفه بنجاح.' % selectedReplay.full_name, 'danger')
        return redirect(url_for('replays', comment_id=comment.id))
    else:
        return render_template('deleteReplay.html', title='حذف | %s' % selectedReplay.full_name,
                                selectedReplay=selectedReplay,
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)



@app.route("/replays/<int:replay_id>/edit/", methods=['GET', 'POST'])
def editReplay(replay_id):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedReplay = Replays.query.filter_by(id=replay_id).one()
    comment = Comments.query.filter_by(id=selectedReplay.comment_id).one()
    if request.method == 'POST':
        if request.form['Full_name']:
            selectedReplay.full_name = request.form['Full_name']
        if request.form['Comment']:
            selectedReplay.comment = request.form['Comment']
        db.session.add(selectedReplay)
        db.session.commit()
        flash('التعليق الخاص ب%s قد تم تعديله بنجاح.' % selectedReplay.full_name, 'info')
        return redirect(url_for('replays', comment_id=comment.id))
    else:
        return render_template('editReplay.html', title='تعديل | %s' % selectedReplay.full_name,
                                selectedReplay=selectedReplay, all_categories=all_categories,
                                all_brands=all_brands, Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)

#=================================================================
#                            Brands
#=================================================================
# for display all brands and it will containing:
#   1-brands[done]. 2-random offers[]. 3-sort by[]. 4-some post[]. 5-random ads[]. 6-search[].
# @app.route("/brands/")
# def brands():
#     all_reviews = Reviews.query.order_by(Reviews.publish_date.desc()).all()
#     allbrands = dict()
#     for brand in all_brands:
#         list_reviews = []
#         for review in all_reviews:
#             if review.brand_id == brand.id:
#                 list_reviews.append(review.id)
#         allbrands[brand.id] = list_reviews
#     return render_template('brands.html', title='العلامات التجارية | لوجامي للتقنية', all_brands=all_brands,
#                             all_reviews=all_reviews, Reviews=Reviews,
#                             all_categories=all_categories,
#                             Categories=Categories, Brands=Brands, allbrands=allbrands)


# route for add a new brand (should login) and it will contain:
#    1-name[done]. 2-image[done]. 3-Ceate button[done].
@app.route("/brands/create/", methods=['GET', 'POST'])
@login_required
def newBrand():         # script[done]    # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    if request.method == 'POST':
        if request.files['Image']:
            image_file = save_brands_picture(request.files['Image'])
        if request.files['Cover']:
            cover_file = save_brands_picture(request.files['Cover'])

        newBrand = Brands(name=request.form['Name'], name_ar=request.form['Name_ar'], 
            image=image_file, cover=cover_file)
        db.session.add(newBrand)
        db.session.commit()
        flash('The new brand has been created!', 'success')
        return redirect(url_for('homepage'))
    else:
        return render_template('newBrand.html', title="اضافة علامة تجارية جديدة | لوجامي للتقنية",
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


# this route will display the details of the selected brand and its contain:
#    1-all review in this brand[done]. 2-some post in this brand[done].
#    3-random offers[]. 4-random ads[].
@app.route("/brands/<int:brand_id>/<string:brand_url>")
def showBrand(brand_id, brand_url):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedBrand = Brands.query.filter_by(id=brand_id).one()
    some_offers = Offers.query.filter_by(brand_id=brand_id).order_by(func.random()).limit(10).all()
    page = request.form.get('page', 1, type=int)
    all_reviews = Reviews.query.filter_by(brand_id=brand_id).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
    return render_template('showBrand.html', title='%s  | لوجامي للتقنية' % selectedBrand.name_ar,
                            pageDescription='تصفح جميع العروض والمراجعات الخاصة بشركة %s' % selectedBrand.name_ar,
                            keywords='تصفح جميع العروض والمراجعات الخاصة بشركة %s'.replace(' ', ', ') % (selectedBrand.name_ar + ' ' + selectedBrand.name),
                            selectedBrand=selectedBrand, all_categories=all_categories,
                            all_reviews=all_reviews, all_brands=all_brands,
                            Categories=Categories, Brands=Brands, brand_id=brand_id,
                            some_offers=some_offers, format=format, float=float, int=int, round=round, Markets=Markets,
                            Post_Types=Post_Types, Users=Users, phone_reviews=phone_reviews,
                            laptop_reviews=laptop_reviews, first_posts=first_posts,
                            second_posts=second_posts, third_posts=third_posts,
                            number_articals=number_articals, number_news=number_news,
                            number_programming=number_programming, number_phones=number_phones,
                            number_laptops=number_laptops)



# this route for edit the selected brand and this contain:
#   1-name[done]. 2-image[done]. 3-Cover[done]. 4-save button[done].
@app.route("/brands/<int:brand_id>/edit/", methods=['GET', 'POST'])
@login_required
def editBrand(brand_id):   # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedBrand = Brands.query.filter_by(id=brand_id).one()
    if request.method == 'POST':
        if request.form['Name']:
            selectedBrand.name = request.form['Name']
        if request.form['Name_ar']:
            selectedBrand.name_ar = request.form['Name_ar']
        if request.files['Image']:

            selectedBrand.image = save_brands_picture(request.files['Image'])
        if request.files['Cover']:
            selectedBrand.cover = save_brands_picture(request.files['Cover'])
        db.session.add(selectedBrand)
        db.session.commit()
        flash('The "%s" brand has been updated!' % selectedBrand.name, 'info')
        return redirect(url_for('homepage'))
    else:
        return render_template('editBrand.html', title='تعديل | %s' % selectedBrand.name_ar,
                                selectedBrand=selectedBrand,
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


# this route for confirm the delete operation for brand and it contain:
#   1-Delete button[done].
@app.route("/brands/<int:brand_id>/delete/", methods=['GET', 'POST'])
@login_required
def deleteBrand(brand_id):    # script[done]    # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedBrand = Brands.query.filter_by(id=brand_id).one()
    if request.method == 'POST':
        db.session.delete(selectedBrand)
        db.session.commit()
        flash('The "%s" has deleted!' % selectedBrand.name, 'danger')
        return redirect(url_for('homepage'))
    else:
        return render_template('deleteBrand.html', title='حذف | %s' % selectedBrand.name_ar,
                                selectedBrand=selectedBrand,
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)



#=================================================================
#                            Reviews
#=================================================================
# for display all brands and it will containing:
#   1-all review[done]. 2-random ads[]. 3-random brand[].
@app.route("/reviews/", methods=['GET', 'POST'])
def reviews():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    random_offers = Offers.query.order_by(func.random()).limit(5).all()
    checkbox_brands = request.form.get('Brand')
    checkbox_categories = request.form.get('Category')
    if request.form.get('search_text'):
        searchReviews = request.form.get('search_text')
    else:
        searchReviews=''

    if request.method == 'POST':
        page = request.form.get('page', 1, type=int)
        if searchReviews is not None:
            if checkbox_brands is not None:
                if checkbox_categories is not None:
                    searched_reviews = Reviews.query.filter(Reviews.name.contains(searchReviews) | Reviews.description.contains(searchReviews)).filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
                else:
                    searched_reviews = Reviews.query.filter(Reviews.name.contains(searchReviews) | Reviews.description.contains(searchReviews)).filter_by(brand_id=checkbox_brands).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
            else:
                if checkbox_categories is not None:
                    searched_reviews = Reviews.query.filter(Reviews.name.contains(searchReviews) | Reviews.description.contains(searchReviews)).filter_by(category_id=checkbox_categories).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
                else:
                    searched_reviews = Reviews.query.filter(Reviews.name.contains(searchReviews) | Reviews.description.contains(searchReviews)).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
        else:
            if checkbox_brands is not None:
                if checkbox_categories is not None:
                    searched_reviews = Reviews.query.filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
                else:
                    searched_reviews = Reviews.query.filter_by(brand_id=checkbox_brands).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
            else:
                if checkbox_categories is not None:
                    searched_reviews = Reviews.query.filter_by(category_id=checkbox_categories).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
                else:
                    searched_reviews = Reviews.query.order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)

        return render_template('reviews.html', title="المراجعات | لوجامي للتقنية", searched_reviews=searched_reviews, searchReviews=searchReviews,
                                    pageDescription='تصفح جميع مراجعاتنا التي تختصر عليك عناء البحث عن تفاصيل الجهاز الذي ترغب بشرائه حيث ستساعدك مراجعاتنا لجميع هذه الاجزة من جعلك متأكدا من ان الجهاز الذي تود شراءه هو الانسب لك.',
                                    keywords='تصفح جميع مراجعاتنا التي تختصر عليك عناء البحث عن تفاصيل الجهاز الذي ترغب بشرائه حيث ستساعدك مراجعاتنا لجميع هذه الاجزة من جعلك متأكدا من ان الجهاز الذي تود شراءه هو الانسب لك.'.replace(' ', ', '),
                                    all_categories=all_categories, all_brands=all_brands,
                                    Categories=Categories, Brands=Brands, round=round,
                                    checkbox_brands=checkbox_brands,int=int, float=float,
                                    checkbox_categories=checkbox_categories, Users=Users, phone_reviews=phone_reviews,
                                    laptop_reviews=laptop_reviews, first_posts=first_posts,
                                    second_posts=second_posts, third_posts=third_posts,
                                    number_articals=number_articals, number_news=number_news,
                                    number_programming=number_programming, number_phones=number_phones,
                                    number_laptops=number_laptops, Post_Types=Post_Types,
                                    random_offers=random_offers,
                                    Markets=Markets)
    else:
        page = request.form.get('page', 1, type=int)
        if searchReviews is not None:
            searched_reviews = Reviews.query.filter(Reviews.name.contains(searchReviews) | Reviews.description.contains(searchReviews)).order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
        else:
            searched_reviews = Reviews.query.order_by(Reviews.publish_date.desc()).paginate(page=page, per_page=16)
        return render_template('reviews.html', title="المراجعات | لوجامي للتقنية", searched_reviews=searched_reviews,
                                    all_categories=all_categories, all_brands=all_brands, searchReviews=searchReviews,
                                    Categories=Categories, Brands=Brands, round=round,
                                    checkbox_brands=checkbox_brands, int=int, float=float,
                                    checkbox_categories=checkbox_categories, Users=Users, phone_reviews=phone_reviews,
                                    laptop_reviews=laptop_reviews, first_posts=first_posts,
                                    second_posts=second_posts, third_posts=third_posts,
                                    number_articals=number_articals, number_news=number_news,
                                    number_programming=number_programming, number_phones=number_phones,
                                    number_laptops=number_laptops, Post_Types=Post_Types,
                                    random_offers=random_offers,
                                    Markets=Markets)





# this route will add a new review and it will contain:
#   1-name[done]. 2-description[done]. 3-image[done]. 4-category[done].
#   5-brand[done]. 6-Create button[done].
@app.route("/reviews/newReview/", methods=['GET', 'POST'])
@login_required
def newReview():    # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    return render_template("newReview.html", title="اضافة منتج جديد | لوجامي للتقنية",
                            all_brands=all_brands, all_categories=all_categories,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                first_posts=first_posts, second_posts=second_posts,
                                third_posts=third_posts, number_articals=number_articals,
                                number_news=number_news, number_programming=number_programming,
                                number_phones=number_phones, number_laptops=number_laptops,
                                Categories=Categories, Users=Users, Post_Types=Post_Types)


# this route will add a new review and it will contain:
#   1-name[done]. 2-description[done]. 3-image[done]. 4-category[done].
#   5-brand[done]. 6-Create button[done].
@app.route("/reviews/newPhone/", methods=['GET', 'POST'])
@login_required
def newPhone():    # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_users = Users.query.order_by(Users.full_name).all()
    category = Categories.query.filter_by(id = 1).one()
    if request.method == 'POST':
        brand = Brands.query.filter_by(id = request.form['Brand']).one()
        if request.files['Image']:
            picture_file = save_review_picture(request.files['Image'])
        newReview = Reviews(name=request.form['Name'], description=request.form['Description'],
                              image=picture_file, category_id=request.form['Category'],
                              brand_id=request.form['Brand'], name_ar=request.form['Name_ar'], 
                              content=request.form['Content'], author_id=request.form['Author_ID'])
        db.session.add(newReview)
        db.session.commit()

        allAdvantages = request.form['Advantages']
        addAdvantages = allAdvantages.split('\r\n')
        for advantage in addAdvantages:
            if advantage != "":
                newAdvantages = Advantages(advantage=advantage, product_id=newReview.id)
                db.session.add(newAdvantages)
                db.session.commit()

        allDisadvantages = request.form['Disadvantages']
        addDisadvantages = allDisadvantages.split('\r\n')
        for disadvantage in addDisadvantages:
            if disadvantage != "":
                newDisadvantages = Disadvantages(disadvantage=disadvantage, product_id=newReview.id)
                db.session.add(newDisadvantages)
                db.session.commit()

        addComparePhones = Compare_Phones(screen_size=request.form['Screen_Size'], screen_type=request.form['Screen_Type'], screen_resolution=request.form['Screen_Resolution'], internal_storage_space=request.form['Internal_Storage_Space'], external_storage_space=request.form['External_Storage_Space'], ram=request.form['RAM'], battery_size=request.form['Battery_Size'], fast_charging=request.form['Fast_Charging'], wireless_charging=request.form['Wireless_Charging'], thickness=request.form['Thickness'], height=request.form['Height'], width=request.form['Width'], weight=request.form['Weight'], colors=request.form['Colors'], ports=request.form['Ports'], number_cameras=request.form['Number_Cameras'], cameras_specifications=request.form['Cameras_Specifications'], processor=request.form['Processor'], methods_securing=request.form['Methods_Securing'], os=request.form['OS'], wireless_connectivity=request.form['Wireless_Connectivity'], accessories=request.form['Accessories'], product_id=newReview.id)

        db.session.add(addComparePhones)
        db.session.commit()

        flash('The new "%s" review has been created!' % newReview.name, 'success')
        return redirect(url_for('reviews'))
    else:
        return render_template('newPhone.html', title="اضافة هاتف جديد | لوجامي للتقنية", all_brands=all_brands,
                            all_categories=all_categories, category=category, all_users=all_users,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                            first_posts=first_posts, second_posts=second_posts,
                            third_posts=third_posts, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            Categories=Categories, Users=Users, Post_Types=Post_Types)


# this route will add a new review and it will contain:
#   1-name[done]. 2-description[done]. 3-image[done]. 4-category[done].
#   5-brand[done]. 6-Create button[done].
@app.route("/reviews/newLaptop/", methods=['GET', 'POST'])
@login_required
def newLaptop():    # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_users = Users.query.order_by(Users.full_name).all()
    category = Categories.query.filter_by(id = 3).one()
    if request.method == 'POST':
        brand = Brands.query.filter_by(id = request.form['Brand']).one()
        if request.files['Image']:
            picture_file = save_review_picture(request.files['Image'])
        newReview = Reviews(name=request.form['Name'], description=request.form['Description'],
                              image=picture_file, category_id=request.form['Category'],
                              brand_id=request.form['Brand'], name_ar=request.form['Name_ar'], 
                              content=request.form['Content'], author_id=request.form['Author_ID'])
        db.session.add(newReview)
        db.session.commit()

        allAdvantages = request.form['Advantages']
        addAdvantages = allAdvantages.split('\r\n')
        if allAdvantages is not None:
            for advantage in addAdvantages:
                newAdvantages = Advantages(advantage=advantage, product_id=newReview.id)
                db.session.add(newAdvantages)
                db.session.commit()

        allDisadvantages = request.form['Disadvantages']
        addDisadvantages = allDisadvantages.split('\r\n')
        if allDisadvantages is not None:
            for disadvantage in addDisadvantages:
                newDisadvantages = Disadvantages(disadvantage=disadvantage, product_id=newReview.id)
                db.session.add(newDisadvantages)
                db.session.commit()


        addCompareLaptops = Compare_Laptops(screen_size=request.form['Screen_Size'], screen_type=request.form['Screen_Type'], screen_resolution=request.form['Screen_Resolution'], storage_space=request.form['Storage_Space'], hard_disk_type=request.form['Hard_Disk_Type'], battery_life=request.form['Battery_Life'], thickness=request.form['Thickness'], weight=request.form['Weight'], colors=request.form['Colors'], ports=request.form['Ports'], camera_properties=request.form['Camera_Properties'], processor_type=request.form['Processor_Type'], processor_speed=request.form['Processor_Speed'], ram=request.form['RAM'], graphics_processor=request.form['Graphics_Processor'], security=request.form['Security'], os=request.form['OS'], wireless_connection=request.form['Wireless_Connection'], product_id=newReview.id)
        db.session.add(addCompareLaptops)
        db.session.commit()

        flash('The new "%s" review has been created!' % newReview.name, 'success')
        return redirect(url_for('reviews'))
    else:
        return render_template('newLaptop.html', title="اضافة لابتوب جديد | لوجامي للتقنية", 
                            all_brands=all_brands, all_categories=all_categories, category=category,
                            all_users=all_users,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                            first_posts=first_posts, second_posts=second_posts,
                            third_posts=third_posts, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            Categories=Categories, Users=Users, Post_Types=Post_Types)


# this route will display the details of the selected review and its contain:
#   1-the description of review[done]. 2-image of poduct[done]. 3-advantages & disadvantages[done].
#   4-all offers in the selected review[].
@app.route("/reviews/<int:review_id>/<string:review_url>/", methods=['GET', 'POST'])
def showReview(review_id, review_url):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    
    selectedReview = Reviews.query.filter_by(id=review_id).one()
    all_comments = Comments.query.filter_by(review_id=selectedReview.id).all()
    # review_compare = Reviews.query.order_by(Reviews.name).all()
    if selectedReview.category_id==1:
        comparePhones = Compare_Phones.query.filter_by(product_id=review_id).one()
    elif selectedReview.category_id==3:
        compareLaptops = Compare_Laptops.query.filter_by(product_id=review_id).one()
    category = Categories.query.filter_by(id=selectedReview.category_id).one()
    category_offers = Offers.query.filter_by(category_id=category.id).order_by(func.random()).limit(5).all()
    brand = Brands.query.filter_by(id=selectedReview.brand_id).one()
    brand_offers = Offers.query.filter_by(brand_id=brand.id).order_by(func.random()).limit(5).all()
    advantages = Advantages.query.filter_by(product_id=review_id).all()
    disadvantages = Disadvantages.query.filter_by(product_id=review_id).all()


    related_reviews = Reviews.query.filter_by(brand_id=selectedReview.brand_id).filter(Reviews.id != selectedReview.id).order_by(func.random()).limit(3).all()
    random_phone_offers = Reviews.query.filter_by(category_id=1).order_by(func.random()).limit(5).all()
    latest_posts = Posts.query.order_by(Posts.publish_date.desc()).limit(4).all()
    prev_review = Reviews.query.order_by(Reviews.publish_date.desc()).filter(Reviews.publish_date < selectedReview.publish_date).first()
    next_review = Reviews.query.order_by(Reviews.publish_date).filter(Reviews.publish_date > selectedReview.publish_date).first()

    return render_template('showReview.html', title="مراجعة %s  | لوجامي للتقنية" % selectedReview.name_ar, selectedReview=selectedReview,
                            pageDescription=selectedReview.description,
                            keywords='%s' % (selectedReview.name + ',' + selectedReview.name_ar + ',' + selectedReview.description.replace(' ', ', ')),
                            all_categories=all_categories, advantages=advantages,
                            disadvantages=disadvantages, all_brands=all_brands,
                            category=category, brand=brand, offers=offers,
                            Markets=Markets, Categories=Categories,
                            Brands=Brands, format=format, Reviews=Reviews,
                            round=round, float=float, category_offers=category_offers,
                            brand_offers=brand_offers, 
                            all_comments=all_comments, review_id=selectedReview.id,
                            len=len, Replays=Replays, related_reviews=related_reviews,
                            Users=Users,
                            Post_Types=Post_Types, phone_reviews=phone_reviews,
                            laptop_reviews=laptop_reviews, first_posts=first_posts,
                            second_posts=second_posts, third_posts=third_posts,
                            number_articals=number_articals, number_news=number_news,
                            number_programming=number_programming, number_phones=number_phones,
                            number_laptops=number_laptops, latest_posts=latest_posts,
                            prev_review=prev_review, next_review=next_review)


#=================================================================
#                            Compare Reviews
#=================================================================
@app.route("/compareReviews/<int:category_id>/<string:category_url>/", methods=['GET', 'POST'])
def compareReviews(category_id,category_url):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedCategory = Categories.query.filter_by(id=category_id).one()
    all_reviews = Reviews.query.filter_by(category_id=category_id).order_by(Reviews.name).all()
    if request.method == 'POST':
        all_reviews = Reviews.query.filter_by(category_id=selectedCategory.id).order_by(Reviews.name).all()
        if request.form.get('First_Review'):
            first_Review = Reviews.query.filter_by(id=request.form['First_Review']).one()
            if selectedCategory.id==1:
                firstComparePhones = Compare_Phones.query.filter_by(product_id=first_Review.id).one()
                firstCompareLaptops = ''
            elif selectedCategory.id==3:
                firstCompareLaptops = Compare_Laptops.query.filter_by(product_id=first_Review.id).one()
                firstComparePhones = ''
        else:
            first_Review = ''
            firstCompareLaptops = ''
            firstComparePhones = ''
        if request.form.get('Second_Review'):
            second_Review = Reviews.query.filter_by(id=request.form['Second_Review']).one()
            if selectedCategory.id==1:
                secondComparePhones = Compare_Phones.query.filter_by(product_id=second_Review.id).one()
                secondCompareLaptops = ''
            elif selectedCategory.id==3:
                secondCompareLaptops = Compare_Laptops.query.filter_by(product_id=second_Review.id).one()
                secondComparePhones = ''
        else:
            second_Review = ''
            secondCompareLaptops = ''
            secondComparePhones = ''

            
        if selectedCategory.id==1:
            firstCompareLaptops = ''
            secondCompareLaptops = ''
        elif selectedCategory.id==3:
            firstComparePhones = ''
            secondComparePhones = ''
    else:
        first_Review = ''
        firstComparePhones = ''
        firstCompareLaptops = ''
        second_Review = ''
        secondComparePhones = ''
        secondCompareLaptops = ''


    return render_template('compareReviews.html', title='مقارنة بين %s' % selectedCategory.name_ar,
                            pageDescription='قدمنا لكم في موقع لوجامي للتقنية خاصية المقارنة بين العديد من الاجهزة حيث يمكنك اختيار جهازين لتقوم بمقارنتهما معا وتكون المقارنة بين اللابتوبات وبين الهواتف الذكية',
                            keywords='قدمنا لكم في موقع لوجامي للتقنية خاصية المقارنة بين العديد من الاجهزة حيث يمكنك اختيار جهازين لتقوم بمقارنتهما معا وتكون المقارنة بين اللابتوبات وبين الهواتف الذكية'.replace(' ', ', '),
                            all_categories=all_categories, all_brands=all_brands,
                            phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                            first_posts=first_posts, second_posts=second_posts,
                            third_posts=third_posts, Users=Users, Post_Types=Post_Types,
                            Categories=Categories, number_articals=number_articals,
                            number_news=number_news, number_programming=number_programming,
                            number_phones=number_phones, number_laptops=number_laptops,
                            Reviews=Reviews, first_Review=first_Review, second_Review=second_Review,
                            firstComparePhones=firstComparePhones, firstCompareLaptops=firstCompareLaptops,
                            secondComparePhones=secondComparePhones, secondCompareLaptops=secondCompareLaptops,
                            selectedCategory=selectedCategory, all_reviews=all_reviews)


# this route for edit the selected review and this contain:
#    1-name[done]. 2-description[done]. 3-image[done]. 4-category[done].
#    5-brand[done]. 6-Save button[done].
@app.route("/reviews/<int:review_id>/editPhone/", methods=['GET', 'POST'])
@login_required
def editPhone(review_id):   # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_users = Users.query.order_by(Users.full_name).all()
    selectedReview = Reviews.query.filter_by(id=review_id).one()
    selectedComparePhones = Compare_Phones.query.filter_by(product_id=review_id).one()
    advantages = Advantages.query.filter_by(product_id=review_id).all()
    disadvantages = Disadvantages.query.filter_by(product_id=review_id).all()
    if request.method == 'POST':
        if request.form['Name']:
            selectedReview.name = request.form['Name']
        if request.form['Name_ar']:
            selectedReview.name_ar = request.form['Name_ar']
        if request.form['Author_ID']:
            selectedReview.author_id = request.form['Author_ID']
        
        if request.form['Description']:
            selectedReview.description = request.form['Description']
        if request.form['Category']:
            selectedReview.category_id = request.form['Category']
            category = Categories.query.filter_by(id = request.form['Category']).one()
        if request.form['Brand']:
            selectedReview.brand_id = request.form['Brand']
        if request.form['Content']:
            selectedReview.content = request.form['Content']

        brand = Brands.query.filter_by(id = request.form['Brand']).one()
        if request.files['Image']:
            picture_file = save_review_picture(request.files['Image'])
            selectedReview.image = picture_file
        db.session.add(selectedReview)

        for advantage in advantages:
            if request.form['Advantage-%s' % advantage.id].replace(' ','')!='':
                advantage.advantage = request.form['Advantage-%s' % advantage.id]
                db.session.add(advantage)
            else:
                db.session.delete(advantage)

        for disadvantage in disadvantages:
            if request.form['Disadvantage-%s' % disadvantage.id].replace(' ','')!='':
                disadvantage.disadvantage = request.form['Disadvantage-%s' % disadvantage.id]
                db.session.add(disadvantage)
            else:
                db.session.delete(disadvantage)

        if request.form['Advantages']:
            allAdvantages = request.form['Advantages']
            addAdvantages = allAdvantages.split('\r\n')
            for advantage in addAdvantages:
                if advantage.replace(' ','')!='':
                    newAdvantages = Advantages(advantage=advantage, product_id=selectedReview.id)
                    db.session.add(newAdvantages)
                else:
                    print('')
                    
                

        if request.form['Disadvantages']:
            allDisadvantages = request.form['Disadvantages']
            addDisadvantages = allDisadvantages.split('\r\n')
            for disadvantage in addDisadvantages:
                if disadvantage.replace(' ','')!='':
                    newDisadvantages = Disadvantages(disadvantage=disadvantage, product_id=selectedReview.id)
                    db.session.add(newDisadvantages)
                else:
                    print('')

        if request.form['Screen_Size']:
            selectedComparePhones.screen_size = request.form['Screen_Size']
        if request.form['Screen_Type']:
            selectedComparePhones.screen_type = request.form['Screen_Type']
        if request.form['Screen_Resolution']:
            selectedComparePhones.screen_resolution = request.form['Screen_Resolution']
        if request.form['Internal_Storage_Space']:
            selectedComparePhones.internal_storage_space = request.form['Internal_Storage_Space']
        if request.form['External_Storage_Space']:
            selectedComparePhones.external_storage_space = request.form['External_Storage_Space']
        if request.form['RAM']:
            selectedComparePhones.ram = request.form['RAM']
        if request.form['Battery_Size']:
            selectedComparePhones.battery_size = request.form['Battery_Size']
        if request.form['Fast_Charging']:
            selectedComparePhones.fast_charging = request.form['Fast_Charging']
        if request.form['Wireless_Charging']:
            selectedComparePhones.wireless_charging = request.form['Wireless_Charging']
        if request.form['Thickness']:
            selectedComparePhones.thickness = request.form['Thickness']
        if request.form['Height']:
            selectedComparePhones.height = request.form['Height']
        if request.form['Width']:
            selectedComparePhones.width = request.form['Width']
        if request.form['Weight']:
            selectedComparePhones.weight = request.form['Weight']
        if request.form['Colors']:
            selectedComparePhones.colors = request.form['Colors']
        if request.form['Ports']:
            selectedComparePhones.ports = request.form['Ports']
        if request.form['Number_Cameras']:
            selectedComparePhones.number_cameras = request.form['Number_Cameras']
        if request.form['Cameras_Specifications']:
            selectedComparePhones.cameras_specifications = request.form['Cameras_Specifications']
        if request.form['Processor']:
            selectedComparePhones.processor = request.form['Processor']
        if request.form['Methods_Securing']:
            selectedComparePhones.methods_securing = request.form['Methods_Securing']
        if request.form['OS']:
            selectedComparePhones.os = request.form['OS']
        if request.form['Wireless_Connectivity']:
            selectedComparePhones.wireless_connectivity = request.form['Wireless_Connectivity']
        if request.form['Accessories']:
            selectedComparePhones.accessories = request.form['Accessories']
        db.session.add(selectedComparePhones)
        db.session.commit()
        flash('The "%s" review has been updated!' % selectedReview.name, 'info')
        return redirect(url_for('reviews'))
    else:
        return render_template('editPhone.html', title='تعديل | %s' % selectedReview.name,
                                selectedReview=selectedReview, all_categories=all_categories,
                                all_brands=all_brands, advantages=advantages,
                                disadvantages=disadvantages, all_users=all_users, 
                                selectedComparePhones=selectedComparePhones,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


# this route for edit the selected review and this contain:
#    1-name[done]. 2-description[done]. 3-image[done]. 4-category[done].
#    5-brand[done]. 6-Save button[done].
@app.route("/reviews/<int:review_id>/editLaptop/", methods=['GET', 'POST'])
@login_required
def editLaptop(review_id):   # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_users = Users.query.order_by(Users.full_name).all()
    selectedReview = Reviews.query.filter_by(id=review_id).one()
    selectedCompareLaptop = Compare_Laptops.query.filter_by(product_id=review_id).one()
    advantages = Advantages.query.filter_by(product_id=review_id).all()
    disadvantages = Disadvantages.query.filter_by(product_id=review_id).all()

    if request.method == 'POST':
        if request.form['Name']:
            selectedReview.name = request.form['Name']
        if request.form['Name_ar']:
            selectedReview.name_ar = request.form['Name_ar']
        if request.form['Author_ID']:
            selectedReview.author_id = request.form['Author_ID']
        
        if request.form['Description']:
            selectedReview.description = request.form['Description']
        if request.form['Category']:
            selectedReview.category_id = request.form['Category']
        if request.form['Brand']:
            selectedReview.brand_id = request.form['Brand']
        if request.form['Content']:
            selectedReview.content = request.form['Content']
        category = Categories.query.filter_by(id = request.form['Category']).one()
        brand = Brands.query.filter_by(id = request.form['Brand']).one()
        if request.files['Image']:
            picture_file = save_review_picture(request.files['Image'])
            selectedReview.image = picture_file
        db.session.add(selectedReview)

        for advantage in advantages:
            if request.form['Advantage-%s' % advantage.id]:
                advantage.advantage = request.form['Advantage-%s' % advantage.id]
                db.session.add(advantage)

        for disadvantage in disadvantages:
            if request.form['Disadvantage-%s' % disadvantage.id]:
                disadvantage.disadvantage = request.form['Disadvantage-%s' % disadvantage.id]
                db.session.add(disadvantage)

        if request.form['Advantages']:
            allAdvantages = request.form['Advantages']
            addAdvantages = allAdvantages.split('\r\n')
            for advantage in addAdvantages:
                newAdvantages = Advantages(advantage=advantage, product_id=selectedReview.id)
                db.session.add(newAdvantages)

        if request.form['Disadvantages']:
            allDisadvantages = request.form['Disadvantages']
            addDisadvantages = allDisadvantages.split('\r\n')
            for disadvantage in addDisadvantages:
                newDisadvantages = Disadvantages(disadvantage=disadvantage, product_id=selectedReview.id)
                db.session.add(newDisadvantages)


        if request.form['Screen_Size']:
            selectedCompareLaptop.screen_size = request.form['Screen_Size']
        if request.form['Screen_Type']:
            selectedCompareLaptop.screen_type = request.form['Screen_Type']
        if request.form['Screen_Resolution']:
            selectedCompareLaptop.screen_resolution = request.form['Screen_Resolution']
        if request.form['Storage_Space']:
            selectedCompareLaptop.storage_space = request.form['Storage_Space']
        if request.form['Hard_Disk_Type']:
            selectedCompareLaptop.hard_disk_type = request.form['Hard_Disk_Type']
        if request.form['Battery_Life']:
            selectedCompareLaptop.battery_life = request.form['Battery_Life']
        if request.form['Thickness']:
            selectedCompareLaptop.thickness = request.form['Thickness']
        if request.form['Weight']:
            selectedCompareLaptop.weight = request.form['Weight']
        if request.form['Colors']:
            selectedCompareLaptop.colors = request.form['Colors']
        if request.form['Ports']:
            selectedCompareLaptop.ports = request.form['Ports']
        if request.form['Camera_Properties']:
            selectedCompareLaptop.camera_properties = request.form['Camera_Properties']
        if request.form['Processor_Type']:
            selectedCompareLaptop.processor_type = request.form['Processor_Type']
        if request.form['Processor_Speed']:
            selectedCompareLaptop.processor_speed = request.form['Processor_Speed']
        if request.form['RAM']:
            selectedCompareLaptop.ram = request.form['RAM']
        if request.form['Graphics_Processor']:
            selectedCompareLaptop.graphics_processor = request.form['Graphics_Processor']
        if request.form['Security']:
            selectedCompareLaptop.security = request.form['Security']
        if request.form['OS']:
            selectedCompareLaptop.os = request.form['OS']
        if request.form['Wireless_Connection']:
            selectedCompareLaptop.wireless_connection = request.form['Wireless_Connection']

        db.session.add(selectedCompareLaptop)
        db.session.commit()
        flash('The "%s" review has been updated!' % selectedReview.name, 'info')
        return redirect(url_for('reviews'))
    else:
        return render_template('editLaptop.html', title='تعديل | %s' % selectedReview.name,
                                selectedReview=selectedReview, all_categories=all_categories,
                                all_brands=all_brands, advantages=advantages,
                                disadvantages=disadvantages, all_users=all_users, 
                                selectedCompareLaptop=selectedCompareLaptop,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)

# this route for confirm the delete operation for review and it contain:
#    1-delete button[done].
@app.route("/reviews/<int:review_id>/delete/", methods=['GET', 'POST'])
@login_required
def deleteReview(review_id):  # script[done]    # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedReview = Reviews.query.filter_by(id=review_id).one()
    if request.method == 'POST':
        
        selectedAdvantages = Advantages.query.filter_by(product_id=review_id).all()
        selectedDisadvantages = Disadvantages.query.filter_by(product_id=review_id).all()
        all_comments = Comments.query.filter_by(review_id=review_id).all()
        for comment in all_comments:
            all_replays = Replays.query.filter_by(comment_id=comment.id).all()
            for replay in all_replays:
                db.session.delete(replay)
                db.session.commit()
            db.session.delete(comment)
            db.session.commit()
        for advantage in selectedAdvantages:
            db.session.delete(advantage)
        for disadvantage in selectedDisadvantages:
            db.session.delete(disadvantage)
        if selectedReview.category_id==1:
            selectedComparePhones = Compare_Phones.query.filter_by(product_id=review_id).one()
            db.session.delete(selectedComparePhones)
        if selectedReview.category_id==3:
            selectedCompareLaptops = Compare_Laptops.query.filter_by(product_id=review_id).one()
            db.session.delete(selectedCompareLaptops)
        db.session.delete(selectedReview)
        db.session.commit()
        flash('The "%s" has deleted!' % selectedReview.name, 'danger')
        return redirect(url_for('reviews'))
    else:
        return render_template('deleteReview.html', title='حذف | %s' % selectedReview.name,
                                selectedReview=selectedReview, Categories=Categories,
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users)



#=====================================================================
#                             Offers
#=====================================================================
# display all offers in this page (sholud login) and it will contain:
#   1-all offers[done]. 2-search[done]. 3-sort_by[done].

@app.route("/offers/", methods=['GET', 'POST'])
def offers():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================

    all_markets = Markets.query.all()
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    all_reviews = Reviews.query.order_by(Reviews.name_ar).all()
    all_currencies = Currency_Converter.query.order_by(Currency_Converter.name_ar).all()
    checkbox_brands = request.form.get('Brand', type=int)
    checkbox_colors = request.form.get('Color')
    checkbox_storages = request.form.get('Storage_Space')
    checkbox_markets = request.form.get('Market')
    checkbox_currencies = request.form.get('Currency', type=float)
    checkbox_sort = request.form.get('Sort')
    checkbox_categories = request.form.get('Category')
    checkbox_reviews = request.form.get('Review', type=int)


    if checkbox_currencies is not None:
        selected_currency = Currency_Converter.query.filter_by(id=checkbox_currencies).one()
    else:
        selected_currency = ''
    if request.form.get('search_text'):
        searchOffers = request.form.get('search_text')
    else:
        searchOffers=''

    if request.method == 'POST':
        page = request.form.get('page', 1, type=int)
        

        if searchOffers is not None:
            if checkbox_brands is not None:
                if checkbox_colors is not None:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)
                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)
                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)
                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)
                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)
                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                else:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)

            else:
                if checkbox_colors is not None:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                else:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)

            return render_template('offers.html', title="العروض | لوجامي للتقنية", all_offers=searched_offers, searchOffers=searchOffers,
                                    pageDescription='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.',
                                    keywords='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.'.replace(' ',', '),
                                    all_categories=all_categories, all_brands=all_brands,
                                    Categories=Categories, Brands=Brands, Markets=Markets,
                                    checkbox_brands=checkbox_brands, checkbox_colors=checkbox_colors,
                                    all_colors=all_colors, all_storages=all_storages,
                                    checkbox_storages=checkbox_storages, all_markets=all_markets,
                                    checkbox_markets=checkbox_markets, int=int, float=float, round=round,
                                    all_currencies=all_currencies, checkbox_currencies=checkbox_currencies,
                                    selected_currency=selected_currency, checkbox_categories=checkbox_categories,
                                    checkbox_sort=checkbox_sort, format=format, all_reviews=all_reviews,
                                    checkbox_reviews=checkbox_reviews,
                                    phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                    first_posts=first_posts, second_posts=second_posts,
                                    third_posts=third_posts, Users=Users, Post_Types=Post_Types, number_articals=number_articals,
                                    number_news=number_news, number_programming=number_programming,
                                    number_phones=number_phones, number_laptops=number_laptops)

        else:
            if checkbox_brands is not None:
                if checkbox_colors is not None:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)

                else:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(brand_id=checkbox_brands).order_by(Offers.price.desc()).paginate(page=page, per_page=20)

            else:
                if checkbox_colors is not None:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(storage_space=checkbox_storages).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter_by(color=checkbox_colors).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(color=checkbox_colors).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                else:
                    if checkbox_storages is not None:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter(storage_space=checkbox_storages).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                    else:
                        if checkbox_markets is not None:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.filter_by(market_id=checkbox_markets).order_by(Offers.price.desc()).paginate(page=page, per_page=20)
                        else:
                            if checkbox_sort == 'low':
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.order_by(Offers.price).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.order_by(Offers.price).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.order_by(Offers.price).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.order_by(Offers.price).paginate(page=page, per_page=20)
                            else:
                                if checkbox_categories is not None:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)

                                else:
                                    if checkbox_reviews is not None:
                                        searched_offers = Offers.query.order_by(Offers.price.desc()).filter_by(review_id=checkbox_reviews).paginate(page=page, per_page=20)

                                    else:
                                        searched_offers = Offers.query.order_by(Offers.price.desc()).paginate(page=page, per_page=20)

            return render_template('offers.html', title="العروض | لوجامي للتقنية", all_offers=searched_offers, searchOffers=searchOffers,
                                    pageDescription='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.',
                                    keywords='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.'.replace(' ',', '),
                                    all_categories=all_categories, all_brands=all_brands,
                                    Categories=Categories, Brands=Brands, Markets=Markets,
                                    checkbox_brands=checkbox_brands, checkbox_colors=checkbox_colors,
                                    all_colors=all_colors, all_storages=all_storages,
                                    checkbox_storages=checkbox_storages, all_markets=all_markets,
                                    checkbox_markets=checkbox_markets, int=int, float=float,
                                    all_currencies=all_currencies, round=round,
                                    checkbox_currencies=checkbox_currencies, selected_currency=selected_currency,
                                    checkbox_sort=checkbox_sort, format=format,
                                    checkbox_categories=checkbox_categories, all_reviews=all_reviews,
                                    checkbox_reviews=checkbox_reviews,
                                    phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                    first_posts=first_posts, second_posts=second_posts,
                                    third_posts=third_posts, Users=Users, Post_Types=Post_Types, number_articals=number_articals,
                                    number_news=number_news, number_programming=number_programming,
                                    number_phones=number_phones, number_laptops=number_laptops)

    else:
        page = request.form.get('page', 1, type=int)
        if searchOffers is not None:
            if checkbox_brands is not None:
                searched_offers = Offers.query.filter(brand_id=checkbox_brands).filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)
            else:
                searched_offers = Offers.query.filter(Offers.name.contains(searchOffers) | Offers.name_ar.contains(searchOffers)).order_by(Offers.price.desc()).paginate(page=page, per_page=20)

            return render_template('offers.html', title="العروض | لوجامي للتقنية", all_offers=searched_offers, searchOffers=searchOffers,
                                    pageDescription='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.',
                                    keywords='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.'.replace(' ',', '),
                                    all_categories=all_categories, all_brands=all_brands,
                                    Categories=Categories, Brands=Brands, Markets=Markets,
                                    all_colors=all_colors, all_storages=all_storages,
                                    checkbox_colors=checkbox_colors, checkbox_storages=checkbox_storages,
                                    all_markets=all_markets, checkbox_markets=checkbox_markets, int=int,
                                    checkbox_brands=checkbox_brands, all_currencies=all_currencies,
                                    checkbox_currencies=checkbox_currencies, float=float,
                                    round=round, selected_currency=selected_currency,
                                    checkbox_sort=checkbox_sort, format=format,
                                    checkbox_categories=checkbox_categories, all_reviews=all_reviews,
                                    checkbox_reviews=checkbox_reviews,
                                    phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                    first_posts=first_posts, second_posts=second_posts,
                                    third_posts=third_posts, Users=Users, Post_Types=Post_Types, number_articals=number_articals,
                                    number_news=number_news, number_programming=number_programming,
                                    number_phones=number_phones, number_laptops=number_laptops)
        else:
            if checkbox_brands is not None:
                searched_offers = Offers.query.filter(brand_id=selected_brand).order_by(Offers.price.desc()).filter_by(category_id=checkbox_categories).paginate(page=page, per_page=20)
            else:
                searched_offers = Offers.query.order_by(Offers.price.desc()).paginate(page=page, per_page=20)

            return render_template('offers.html', title="العروض | لوجامي للتقنية", all_offers=searched_offers,
                                    pageDescription='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.',
                                    keywords='الان يمكنك مقارنة اسعار الاجهزة بين مختلف المتاجر الالكترونية مثل amazom و eBay وSouq.com وغيرها من المتاجر المختلفة.'.replace(' ',', '),
                                    all_categories=all_categories, all_brands=all_brands,
                                    Categories=Categories, Brands=Brands, Markets=Markets,
                                    all_colors=all_colors, all_storages=all_storages,
                                    checkbox_colors=checkbox_colors, checkbox_storages=checkbox_storages,
                                    all_markets=all_markets, checkbox_markets=checkbox_markets, int=int,
                                    checkbox_brands=checkbox_brands, all_currencies=all_currencies,
                                    checkbox_currencies=checkbox_currencies, float=float,
                                    round=round, selected_currency=selected_currency,
                                    checkbox_sort=checkbox_sort, format=format,
                                    checkbox_categories=checkbox_categories, all_reviews=all_reviews,
                                    checkbox_reviews=checkbox_reviews,
                                    phone_reviews=phone_reviews, laptop_reviews=laptop_reviews,
                                    first_posts=first_posts, second_posts=second_posts,
                                    third_posts=third_posts, Users=Users, Post_Types=Post_Types, number_articals=number_articals,
                                    number_news=number_news, number_programming=number_programming,
                                    number_phones=number_phones, number_laptops=number_laptops)


#=====================================================================
#                             Check Offers
#=====================================================================
# display all offers in this page (sholud login) and it will contain:
#   1-all offers[]. 2-search[]. 3-sort_by[]. 4-display old and new price[].
#   5-display iframe window for each offer to change the details[].
#   6-

@app.route("/checkOffers/", methods=['GET', 'POST'])
@login_required
def checkOffers():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    all_reviews = Reviews.query.all()
    all_markets = Markets.query.all()
    page = request.form.get('page', 1, type=int)
    all_offers = Offers.query.filter(Offers.checked.isnot('True')).order_by(Offers.id.desc()).paginate(page=page, per_page=12)
    return render_template('checkOffers.html', title="تحديث بيانات العروض | لوجامي للتقنية",
                            all_brands=all_brands, all_categories=all_categories,
                            all_markets=all_markets, all_reviews=all_reviews,
                            all_colors=all_colors, all_storages=all_storages,
                            all_offers=all_offers, float=float, int=int,
                            round=round, Markets=Markets,
                            Post_Types=Post_Types, phone_reviews=phone_reviews,
                            laptop_reviews=laptop_reviews, first_posts=first_posts,
                            second_posts=second_posts, third_posts=third_posts,
                            number_articals=number_articals, number_news=number_news,
                            number_programming=number_programming, number_phones=number_phones,
                            number_laptops=number_laptops, Users=Users, Categories=Categories)

@app.route("/offers/checkAllOffers/", methods=['GET', 'POST'])
@login_required
def checkAllOffers():
    all_offers = Offers.query.filter(Offers.checked!='True').all()
    for offer in all_offers:
        selectedOffer = Offers.query.filter_by(id=offer.id).first()
        selectedOffer.checked = 'True'
        db.session.add(selectedOffer)
        db.session.commit()
    return redirect(url_for('checkOffers'))

@app.route("/offers/uncheckAllOffers/", methods=['GET', 'POST'])
@login_required
def uncheckAllOffers():
    all_offers = Offers.query.all()
    for offer in all_offers:
        selectedOffer = Offers.query.filter_by(id=offer.id).first()
        selectedOffer.checked = ''
        db.session.add(selectedOffer)
        db.session.commit()
    return redirect(url_for('checkOffers'))


@app.route("/offers/<int:offer_id>/check/", methods=['GET', 'POST'])
@login_required
def checkedOffers(offer_id):
    selectedOffer = Offers.query.filter_by(id=offer_id).one()
    selectedOffer.checked = 'True'
    db.session.add(selectedOffer)
    db.session.commit()
    flash('The "%s" has checked!' % selectedOffer.name, 'success')
    return redirect(url_for('checkOffers'))


###############################################################################################

# # here you will can ceate a new offer and this page is contain:
# #   1-name[done]. 2-description[done]. 3-image[done]. 4-category[done]. 5-brand[done].
# #   6-market[]. 7-price[]. 8-url[]. 9-Create button[].

@app.route("/offers/create/", methods=['GET', 'POST'])
@login_required
def newOffer():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    all_reviews = Reviews.query.all()
    all_markets = Markets.query.all()
    if request.method == 'POST':
        category = Categories.query.filter_by(id = request.form['Category']).one()
        brand = Brands.query.filter_by(id = request.form['Brand']).one()
        newOffer = Offers(name=request.form['Name'], image=request.form['Image'], price=request.form['Price'],
                          category_id=request.form['Category'], brand_id=request.form['Brand'],
                          market_id=request.form['Market'], url=request.form['Url'], color=request.form['Color'],
                          storage_space=request.form['Storage_Space'],
                          name_ar=request.form['Name_ar'], review_id=request.form['Review'])
        db.session.add(newOffer)
        db.session.commit()

        flash('The new "%s" offer has been created!' % newOffer.name, 'success')
        return redirect(url_for('offers'))
    else:
        return render_template('newOffer.html', title="اضافة عرض جديد | لوجامي للتقنية", all_brands=all_brands,
                                all_categories=all_categories, all_markets=all_markets,
                                all_reviews=all_reviews, all_colors=all_colors,
                                all_storages=all_storages,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


# # this route will display the details of the selected offer and its contain:
# # 1-name[]. 2-image[]. 3-description[]. 4-urls[]. 5-price[].
# @app.route("/offers/<int:offer_id>/")
# def showOffer(offer_id):
#   return 'display details of the select offer'

# # this route will display the details of the selected offer and its contain:
# # 1-name[]. 2-description[]. 3-image[]. 4-category[]. 5-brand[].
# # 6-market[]. 7-pice[]. 8-url[].
@app.route("/offers/<int:offer_id>/edit/", methods=['GET', 'POST'])
@login_required
def editOffer(offer_id):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedOffer = Offers.query.filter_by(id=offer_id).one()
    all_markets = Markets.query.all()
    all_reviews = Reviews.query.all()
    all_colors = Colors.query.all()
    all_storages = Storage_Space.query.all()
    if request.method == 'POST':
        if request.form['Name']:
            selectedOffer.name = request.form['Name']
        if request.form['Url']:
            selectedOffer.url = request.form['Url']
        if request.form['Category']:
            selectedOffer.category_id = request.form['Category']
        if request.form['Brand']:
            selectedOffer.brand_id = request.form['Brand']
        if request.form['Review']:
            selectedOffer.review_id = request.form['Review']
        if request.form['Color']:
            selectedOffer.color = request.form['Color']
        if request.form['Storage_Space']:
            selectedOffer.storage_space = request.form['Storage_Space']
        if request.form['Market']:
            selectedOffer.market_id = request.form['Market']
        if request.form['Price']:
            selectedOffer.price = request.form['Price']
            selectedOffer.price = request.form['Price']
        category = Categories.query.filter_by(id = request.form['Category']).one()
        brand = Brands.query.filter_by(id = request.form['Brand']).one()

        db.session.add(selectedOffer)
        db.session.commit()
        flash('The "%s" offer has been updated!' % selectedOffer.name, 'info')
        return redirect(url_for('offers'))
    else:
        return render_template('editOffer.html', title='تعديل | %s' % selectedOffer.name,
                                selectedOffer=selectedOffer, all_categories=all_categories,
                                all_brands=all_brands, all_markets=all_markets,
                                all_reviews=all_reviews, all_colors=all_colors,
                                all_storages=all_storages,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


# # this route for confirm the delete operation for offer and it contain:
# #    1-delete button[].
@app.route("/offers/<int:offer_id>/delete/", methods=['GET', 'POST'])
@login_required
def deleteOffer(offer_id):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedOffer = Offers.query.filter_by(id=offer_id).one()
    if request.method == 'POST':
        db.session.delete(selectedOffer)
        db.session.commit()
        flash('The "%s" has deleted!' % selectedOffer.name, 'danger')
        return redirect(url_for('offers'))
    else:
        return render_template('deleteOffer.html', title='حذف | %s' % selectedOffer.name,
                                selectedOffer=selectedOffer,
                                all_categories=all_categories, all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


#=========================================================================
#                                  Posts
#=========================================================================
# this route will display all post and it will contain:
#   1-all post[done]. 2-sort by[]. 3-search[]. *4-delete button[done].* *5-add button[done].*
#   *6-edit button[done].* 7-random ads[].
@app.route("/posts/", methods=['GET', 'POST'])
def posts():
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    if request.form.get('search_text'):
        searchPosts = request.form.get('search_text')
    else:
        searchPosts=''
    random_offers = Offers.query.order_by(func.random()).limit(5).all()
    all_post_types = Post_Types.query.all()
    checkbox_brands = request.form.get('Brand')
    checkbox_sort = request.form.get('Sort')
    checkbox_categories = request.form.get('Category')
    checkbox_post_types = request.form.get('Post_Type', type=int)
    if request.method == 'POST':
        page = request.form.get('page', 1, type=int)
        if searchPosts is not None:
            if checkbox_brands is not None:
                if checkbox_categories is not None:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                else:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(brand_id=checkbox_brands).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
            else:
                if checkbox_categories is not None:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(category_id=checkbox_categories).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(category_id=checkbox_categories).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                else:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
        else:
            if checkbox_brands is not None:
                if checkbox_categories is not None:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).order_by(Posts.publish_date).paginate(page=page, per_page=12)

                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).filter_by(category_id=checkbox_categories).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)

                else:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).order_by(Posts.publish_date).paginate(page=page, per_page=12)

                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter_by(brand_id=checkbox_brands).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
            else:
                if checkbox_categories is not None:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter_by(category_id=checkbox_categories).order_by(Posts.publish_date).paginate(page=page, per_page=12)

                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(category_id=checkbox_categories).filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.filter_by(category_id=checkbox_categories).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                else:
                    if checkbox_sort == 'old':
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.order_by(Posts.publish_date).paginate(page=page, per_page=12)

                    else:
                        if checkbox_post_types is not None:
                            searched_post = Posts.query.filter_by(post_type_id=checkbox_post_types).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)
                        else:
                            searched_post = Posts.query.order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)

        return render_template('posts.html', title="المنشورات | لوجامي للتقنية", all_posts=searched_post, searchPosts=searchPosts,
                                pageDescription='تصفح العديد من المقالات المتنوعة والمتخصصة في مجالات عديدة مثل البرمجة وجديد التقنية وتفاصيل الاجهزة المتنوعة وحلول مشاكل تقنية منتشرة بين مختلف الناس.',
                                keywords='تصفح العديد من المقالات المتنوعة والمتخصصة في مجالات عديدة مثل البرمجة وجديد التقنية وتفاصيل الاجهزة المتنوعة وحلول مشاكل تقنية منتشرة بين مختلف الناس.'.replace(' ',', '),
                                all_categories=all_categories, all_brands=all_brands,
                                Categories=Categories, Brands=Brands, Markets=Markets,
                                checkbox_brands=checkbox_brands, checkbox_categories=checkbox_categories,
                                checkbox_sort=checkbox_sort, int=int, float=float, round=round,
                                all_post_types=all_post_types, checkbox_post_types=checkbox_post_types,
                                Post_Types=Post_Types, Users=Users,
                                phone_reviews=phone_reviews, random_offers=random_offers,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops)
    else:
        page = request.form.get('page', 1, type=int)
        if searchPosts is not None:
            searched_post = Posts.query.filter(Posts.title.contains(searchPosts) | Posts.content.contains(searchPosts)).order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)

        else:
            searched_post = Posts.query.order_by(Posts.publish_date.desc()).paginate(page=page, per_page=12)

        return render_template('posts.html', title="المنشورات | لوجامي للتقنية", all_posts=searched_post,
                                pageDescription='تصفح العديد من المقالات المتنوعة والمتخصصة في مجالات عديدة مثل البرمجة وجديد التقنية وتفاصيل الاجهزة المتنوعة وحلول مشاكل تقنية منتشرة بين مختلف الناس.',
                                keywords='تصفح العديد من المقالات المتنوعة والمتخصصة في مجالات عديدة مثل البرمجة وجديد التقنية وتفاصيل الاجهزة المتنوعة وحلول مشاكل تقنية منتشرة بين مختلف الناس.'.replace(' ',', '),
                                all_categories=all_categories, all_brands=all_brands,
                                Categories=Categories, Brands=Brands, Markets=Markets,
                                checkbox_brands=checkbox_brands, checkbox_categories=checkbox_categories,
                                checkbox_sort=checkbox_sort, int=int, float=float, round=round,
                                all_post_types=all_post_types,checkbox_post_types=checkbox_post_types,
                                Post_Types=Post_Types, Users=Users,
                                phone_reviews=phone_reviews, random_offers=random_offers,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops)


# here you will can ceate a new post and this page is contain:
#   1-title[done]. 2-content[done]. 3-image[done]. 4-publish_date[x]. 5-category[done].
#   6-brand[done]. 7-create button[done].
@app.route("/posts/newPost/", methods=['GET', 'POST'])
@login_required
def newPost():     # script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    all_post_types = Post_Types.query.all()
    all_users = Users.query.order_by(Users.full_name).all()
    if request.method == 'POST':
        # category = Categories.query.filter_by(id=request.form['Category']).one()
        if request.files['Image']:
            picture_file = save_post_picture(request.files['Image'])

        newPost = Posts(title=request.form['Title'], content=request.form['Content'],
                        image=picture_file, post_type_id=request.form['Post_Type'],
                        description=request.form['Description'], author_id=request.form['Author_ID'])
        db.session.add(newPost)
        db.session.commit()
        flash('The new "%s" review has been created!' % newPost.title, 'success')
        return redirect(url_for('posts'))
    else:
        return render_template('newPost.html', title="اضافة منشور جديد | لوجامي للتقنية",
                                all_brands=all_brands, all_categories=all_categories,
                                all_post_types=all_post_types, all_users=all_users,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)



# this route will display the details of the selected post and its contain:
#   1-title[done]. 2-content[done]. 3-image[done]. 4-random ads[].
#   *5-edit button[].* *6-delete button[].* *7-add button[].*
@app.route("/posts/<int:post_id>/<string:post_url>/")
def showPost(post_id, post_url):
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    selectedPost = Posts.query.filter_by(id=post_id).one()
    # category = Categories.query.filter_by(id=selectedPost.category_id).one()
    related_posts = Posts.query.filter_by(post_type_id=selectedPost.post_type_id).filter(Posts.id != selectedPost.id).limit(3).all()
    all_comments = Comments.query.filter_by(post_id=selectedPost.id).order_by(Comments.publish_date.desc()).all()
    random_phone_offers = Offers.query.filter_by(category_id=1).order_by(func.random()).limit(5).all()
    latest_reviews = Reviews.query.order_by(Reviews.publish_date.desc()).limit(4).all()
    prev_post = Posts.query.order_by(Posts.publish_date.desc()).filter(Posts.publish_date < selectedPost.publish_date).first()
    next_post = Posts.query.order_by(Posts.publish_date).filter(Posts.publish_date > selectedPost.publish_date).first()
    return render_template('showPost.html', title='%s | لوجامي للتقنية' % selectedPost.title,
                            pageDescription=selectedPost.description,
                            keywords=selectedPost.description.replace(' ', ', '),
                            selectedPost=selectedPost, all_categories=all_categories,
                            all_brands=all_brands, related_posts=related_posts,
                            float=float, len=len,
                            round=round, Users=Users, all_comments=all_comments,
                            Markets=Markets, Categories=Categories,
                            Post_Types=Post_Types, phone_reviews=phone_reviews,
                            laptop_reviews=laptop_reviews, first_posts=first_posts,
                            second_posts=second_posts, third_posts=third_posts,
                            Replays=Replays, random_phone_offers=random_phone_offers,
                            number_articals=number_articals, number_news=number_news,
                            number_programming=number_programming, number_phones=number_phones,
                            number_laptops=number_laptops, latest_reviews=latest_reviews,
                            prev_post=prev_post, next_post=next_post)


# this route will display the details of the selected post and its contain:
#   1-title[done]. 2-content[done]. 3-image[done]. 4-publish_date[x]. 5-category[done].
#   6-brand[done]. 7-save button[done].
@app.route("/posts/<int:post_id>/edit/", methods=['GET', 'POST'])
@login_required
def editPost(post_id):      # script[done]    # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedPost = Posts.query.filter_by(id=post_id).one()
    all_post_types = Post_Types.query.all()
    all_users = Users.query.order_by(Users.full_name).all()
    if request.method == 'POST':
        if request.form['Title']:
            selectedPost.title = request.form['Title']
        if request.form['Content']:
            selectedPost.content = request.form['Content']
        if request.form['Description']:
            selectedPost.description = request.form['Description']
        # category = Categories.query.filter_by(id = request.form['Category']).one()
        if request.form['Author_ID']:
            selectedPost.author_id = request.form['Author_ID']
        if request.form['Post_Type']:
            selectedPost.post_type_id = request.form['Post_Type']

        if request.files['Image']:
            picture_file = save_post_picture(request.files['Image'])
            selectedPost.image = picture_file

        db.session.add(selectedPost)
        db.session.commit()
        flash('The "%s" brand has been updated!' % selectedPost.title, 'info')
        return redirect(url_for('posts'))
    else:
        return render_template('editPost.html', title='نعديل | %s' % selectedPost.title,
                                selectedPost=selectedPost, all_categories=all_categories,
                                all_brands=all_brands, all_post_types=all_post_types,
                                all_users=all_users,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


# this route for confirm the delete operation for post and it contain:
#    1-delete button[done].
@app.route("/posts/<int:post_id>/delete/", methods=['GET', 'POST'])
@login_required
def deletePost(post_id):    #script[done]   # style[done]
    all_categories = Categories.query.all()
    all_brands = Brands.query.all()
    phone_reviews = Reviews.query.filter_by(category_id=1).order_by(Reviews.publish_date.desc()).limit(3).all()
    laptop_reviews = Reviews.query.filter_by(category_id=3).order_by(Reviews.publish_date.desc()).limit(3).all()
    first_posts = Posts.query.filter_by(post_type_id=1).order_by(Posts.publish_date.desc()).limit(4).all()
    second_posts = Posts.query.filter_by(post_type_id=2).order_by(Posts.publish_date.desc()).limit(4).all()
    third_posts = Posts.query.filter_by(post_type_id=3).order_by(Posts.publish_date.desc()).limit(4).all()
    number_articals = len(Posts.query.filter_by(post_type_id=2).all())
    number_news = len(Posts.query.filter_by(post_type_id=1).all())
    number_programming = len(Posts.query.filter_by(post_type_id=3).all())
    number_phones = len(Reviews.query.filter_by(category_id=1).all())
    number_laptops = len(Reviews.query.filter_by(category_id=3).all())
    #==================================================================================
    #==================================================================================
    selectedPost = Posts.query.filter_by(id=post_id).one()
    if request.method == 'POST':
        db.session.delete(selectedPost)
        db.session.commit()
        flash('The "%s" has deleted!' % selectedPost.title, 'danger')
        return redirect(url_for('posts'))
    else:
        return render_template('deletePost.html', title='حذف | %s' % selectedPost.title,
                                selectedPost=selectedPost, all_categories=all_categories,
                                all_brands=all_brands,
                                Post_Types=Post_Types, phone_reviews=phone_reviews,
                                laptop_reviews=laptop_reviews, first_posts=first_posts,
                                second_posts=second_posts, third_posts=third_posts,
                                number_articals=number_articals, number_news=number_news,
                                number_programming=number_programming, number_phones=number_phones,
                                number_laptops=number_laptops, Users=Users, Categories=Categories)


#=======================================================================
#=======================================================================


if __name__ == '__main__':
    app.secret_key = 'Super_Secret_Key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    bcrypt = Bcrypt(app)
    app.debug = True

    app.run()
