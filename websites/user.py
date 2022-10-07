
from unicodedata import category
from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from . import db
import json
from bson.objectid import ObjectId

user = Blueprint("user", __name__)

@user.route('/profile')
def profile():

    if "logged" not in session:
        return redirect(url_for('auth.log_in'))

    all_product_owned = db.product.find({"owner":session['user_email']})
    
    return render_template('profile.html', email=session['user_email'], all_product_owned = all_product_owned)








@user.route('/profile/add_product', methods=["POST", "GET"])
def add_product():

    if request.method == "POST":
        
        # get the request
        title = request.form.get('product_title')
        category = request.form.get('product_category')
        price = request.form.get('product_price')
        description = request.form.get('product_description')
        owner = session['user_email']

        # define a product 
        p = {
            "owner":owner,
            "title":title, 
            "category":category, 
            "price":price, 
            "description":description
        }

        # update db
        db.product.insert_one(p)

        # redirect to profile
        flash('Product Add!', category='success')
        return redirect(url_for('user.profile'))

    return render_template('add_product.html')

@user.route('/profile/update/')
def update():
    return "update product"

@user.route('/profile/delete/<product_id>')
def delete(product_id):

    # use object id to remove one product from db.product
    object_id = ObjectId(product_id)
    db.product.delete_one({"_id":object_id})
    flash('product delete!', category='success')

    return redirect(url_for('user.profile'))