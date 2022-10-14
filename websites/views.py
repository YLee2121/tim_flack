from flask import Blueprint, render_template, redirect, url_for, session
from . import db
from bson.objectid import ObjectId

views = Blueprint("views", __name__)




@views.route("/")
def home():

    if "logged" not in session:
        return redirect(url_for('auth.log_in'))

    all_product = db.product.find({})
    all_product = list(all_product) # turn into list can make html iteration easiler


    return render_template("home.html", all_product_online=all_product)

@views.route("/about")
def about(): 
    return render_template("about.html")

@views.route("/filter_by/<category>")
def filter_by(category):
    all_product = db.product.find({'category':category})
    all_product = list(all_product) # into list can make html iteration easiler
    return render_template("home.html", all_product_online=all_product)

@views.route("/product/<product_id>")
def click_pic(product_id):

    # use object id to remove one product from db.product
    object_id = ObjectId(product_id)
    p = db.product.find_one({"_id":object_id})
    
    return render_template('product_detail.html', product=p)




