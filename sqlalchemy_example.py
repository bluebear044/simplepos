#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=False, nullable=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User[%s] %s, %s>' % (self.id, self.username, self.email)

class Product(db.Model):
    product_code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    product_desc = db.Column(db.String(500), nullable=True)
    product_price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, default=0)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    use_yn = db.Column(db.String(1), default='Y')

    def __init__(self, product_name, product_desc, product_price):
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_price = product_price

    def __repr__(self):
        return '<Product %s : %s : %s>' % (self.product_code, self.product_name, self.product_price)

class Sale(db.Model):
    sale_code = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.Integer, db.ForeignKey("product.product_code"), primary_key=True)
    product = db.relationship('Product', backref='sales')
    sale_quantity = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Integer, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,sale_code, product_code, sale_quantity, sale_price):
        self.sale_code = sale_code
        self.product_code = product_code
        self.sale_quantity = sale_quantity
        self.sale_price = sale_price

    def __repr__(self):
        return '<Sale %s : %s : %s : %s>' % (self.sale_code, self.product_code, self.sale_quantity, self.sale_price)


if __name__ == "__main__":
    #initial
    db.drop_all()
    db.create_all()

    admin = User('admin', 'admin@example.com')
    guest1 = User('guest1', 'guest1@example.com')
    guest2 = User('guest2', 'guest2@example.com')
    guest3 = User('guest3', 'guest3@example.com')

    #delete all
    db.session.query(User).delete()

    #insert
    db.session.add(admin)
    db.session.add(guest1)
    db.session.add(guest2)
    db.session.add(guest3)

    #delete
    db.session.query(User).filter(User.username == 'guest3').delete()

    #update
    db.session.query(User).filter(User.username == 'admin').update({'email': 'hahaha'})

    #commit
    db.session.commit()

    #select
    users = User.query.all()
    print users

    ##############################################################
    product1 = Product('tent', 'this is good tent', 5000)
    product2 = Product('hammer', 'this is good hammer', 9000)
    product3 = Product('niddle', 'this is good niddle', 100)

    db.session.query(Product).delete()
    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)

    db.session.commit()

    #select
    products = Product.query.all()
    print products

    ##############################################################
    # 1:M insert

    sale1 = Sale(9999, 1, 3, 15000)
    sale2 = Sale(9999, 2, 3, 27000)
    db.session.query(Sale).delete()
    db.session.add(sale1)
    db.session.add(sale2)

    #select
    sales = Sale.query.all()
    print sales

    print sales[0].product
    print sales[1].product

############################
# API Documents
# http://docs.sqlalchemy.org/en/latest/orm/query.html#the-query-object
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships
# http://stackoverflow.com/questions/16433338/inserting-new-records-with-one-to-many-relationship-in-flask-sqlalchemy
# http://haruair.com/blog/1695
############################