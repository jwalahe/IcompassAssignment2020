'''
ICompass Assignment: Jwala Kompalli

Here is a simple Flask API where we can send CRUD requests to a database which has information about various products.

I took the liberty of changing the json response if the input payload doesn't have any characters that is pertaining to the SQL Injection attacks. 
We will simply get a dump of products inside the database instead of 'sanitized' response!

We can also access single products from the data base and I implemented another sanitization check there to see if the input is sanitized or not.

I have used the Flask, SQLALchemy and Marshmallow libraries to implement the below API

'''

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initialize App
app=Flask(__name__)

#This will store the absolute path for Database File. Hence we use 'os' package
basedir = os.path.abspath(os.path.dirname(__file__))

#Database Setup
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#Initialize Database
db=SQLAlchemy(app)

#Initialize Marshmallow
ma = Marshmallow(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/v1/sanitized/input',methods=['POST'])
def add_product():
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    quantity=request.json['quantity']

    list_of_sql_injection_characters =["1==1",";","=",'" OR ""="',] #These are some of the common characters in the sql-Injection attacks

    #Chekcing whether the inputs are sanitized or not
    for chars in list_of_sql_injection_characters:
        if str(chars) in name or str(chars) in description or str(chars) in str(price) or str(chars) in str(quantity):
            return jsonify('not_sanitized')
    
    new_product=Product(name,description,price,quantity)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product) 


#Get All Products
@app.route('/v1/sanitized/input',methods=['GET'])
def get_products():
    all_products=Product.query.all()
    result=products_schema.dump(all_products)
    return jsonify(result)

#This feteches a single product
@app.route('/v1/sanitized/input/<id>',methods=['GET'])
def get_product(id):
    list_of_sql_injection_characters =["1==1",";","=",'" OR ""="',] #These are some of the common characters in the sql-Injection attacks
    if str(id) in list_of_sql_injection_characters: #I believe that this is not necessary, since Id is the primary key and we cannot pass string values. Marhsmallow will throw a type error!
        return jsonify('not sanitized')

    product=Product.query.get(id)
    if product is None:
        return jsonify('Not in database')
    return product_schema.jsonify(product)

#This is an update 
@app.route('/v1/sanitized/input/<id>',methods=['PUT'])
def update_product(id):
    product=Product.query.get(id)
    name=request.json['name']
    description=request.json['description']
    price=request.json['price']
    quantity=request.json['quantity']

    list_of_sql_injection_characters =["1==1",";","=",'" OR ""="',] #These are some of the common characters in the sql-Injection attacks

    #Chekcing whether the inputs are sanitized or not
    for chars in list_of_sql_injection_characters:
        if str(chars) in name or str(chars) in description or str(chars) in str(price) or str(chars) in str(quantity):
            return jsonify('not_sanitized')
    
    product.name=name
    product.description=description
    product.price=price
    product.quantity=quantity

    db.session.commit()
    return product_schema.jsonify(product) 

@app.route('/v1/sanitized/input/<id>',methods=['DELETE'])
def delete_product(id):
    list_of_sql_injection_characters =["1==1",";","=",'" OR ""="',] #These are some of the common characters in the sql-Injection attacks
    if str(id) in list_of_sql_injection_characters: #I believe that this is not necessary, since Id is the primary key and we cannot pass string values. Marhsmallow will throw a type error!
        return jsonify('not sanitized')

    product=Product.query.get(id)
    if product is None:
        return jsonify('Not in database')
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

# Run Server
if __name__=='__main__':
    app.run(debug=True)

