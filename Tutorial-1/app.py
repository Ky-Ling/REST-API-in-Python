'''
Date: 2022-02-26 16:42:08
LastEditors: GC
LastEditTime: 2022-02-26 21:41:16
FilePath: \REST API\app.py
'''

# When we have a REST API, for the most part we are going to return JSON data.
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Database
#   This is going to look for a file called db.sqlite in the current folder structure
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Produce class/Model
class Product(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
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
        fields = ("id", "name", "description", "price", "qty")

# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product)
    
# Get all products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)

    return jsonify(result.data)

# Get single product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)


# Update the product
@app.route("/product/<id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get(id)

    # Get all of our fields from the body of the request
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    qty = request.json["qty"]
 
    # Construct a new product to submit to the database
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()
    
    return product_schema.jsonify(product)


# Delete the product
@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()


    return product_schema.jsonify(product)



# Run server
if __name__ == "__main__":
    db.create_all()
    print("Create the database")

    app.run(debug=True)
