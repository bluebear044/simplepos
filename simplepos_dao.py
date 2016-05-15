#!/usr/bin/python
# -*- coding:utf-8 -*-

from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simplepos.db'
db = SQLAlchemy(app)

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
        return '<Product code : %s name : %s price : %s>' % (self.product_code, self.product_name, self.product_price)

class Sale(db.Model):
    sale_code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.String(32))
    product_code = db.Column(db.Integer, db.ForeignKey("product.product_code"))
    product = db.relationship('Product', backref='sales')
    sale_quantity = db.Column(db.Integer, nullable=False)
    sale_price = db.Column(db.Integer, nullable=False)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_yn = db.Column(db.String(1), default='N')

    def __init__(self,tid, product_code, sale_quantity, sale_price):
        self.tid = tid
        self.product_code = product_code
        self.sale_quantity = sale_quantity
        self.sale_price = sale_price

    def __repr__(self):
        return '<Sale code : %s tid : %s product_code : %s quantity : %s price : %s end_yn : %s>' % (self.sale_code, self.tid, self.product_code, self.sale_quantity, self.sale_price, self.end_yn)


def selectProduct() :
    return Product.query.order_by(desc(Product.product_code)).all()


def selectSale() :
    return Sale.query.order_by(desc(Sale.reg_date)).all()


def insertProduct(productName, productPrice) :
    item = Product(productName, '', productPrice)
    db.session.add(item)
    db.session.commit()


def deleteProduct(productCode) :
    db.session.query(Product).filter(Product.product_code == productCode).delete()
    db.session.commit()


def insertSale(tid, productCode, saleQuantity, salePrice) :
    item = Sale(tid, productCode, saleQuantity, salePrice)
    db.session.add(item)
    db.session.commit()

def updateSale() :
    db.session.query(Sale).update({'end_yn': 'Y'})

def initailDB() :
    db.drop_all()
    db.create_all()