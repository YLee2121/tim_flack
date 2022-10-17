
from flask import Blueprint, render_template, redirect, url_for, session, request, flash, jsonify
from . import db, APP_TO_PIC_PATH, SRC_TO_PIC_PATH, allowed_file
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.utils import secure_filename
import os


user = Blueprint("user", __name__)

@user.route('/profile')
def profile():

    if "logged" not in session:
        return redirect(url_for('auth.log_in'))

    all_product_owned = db.product.find({"owner":session['user_email']})
    
    
    return render_template('profile.html', email=session['user_email'], all_product_owned = all_product_owned)








@user.route('/profile/add_product', methods=["POST", "GET"])
def add_product():

    if request.method != "POST":
        return render_template('add_product.html')
        
    # get the request
    title = request.form.get('product_title')
    category = request.form.get('product_category')
    price = request.form.get('product_price')
    description = request.form.get('product_description')
    owner = session['user_email']
    post_date = str(datetime.now().date())
            
            

    ##### pic processing

    pic_name = str(datetime.now()) + secure_filename(request.files['product_pic'].filename) # add a datetime.now(), to make the name unique
    product_pic = request.files['product_pic']

    # check extension 
    if not allowed_file(pic_name):
        flash('Image format not allowed!', category='error')
        return render_template('add_product.html')

    # check dir app.py viewpoint


    personal_dir = APP_TO_PIC_PATH + session['user_email'] + '/'
    if not os.path.exists(personal_dir):
        os.mkdir(personal_dir)

    save_path = personal_dir + pic_name
    path_for_html = f'../{SRC_TO_PIC_PATH}' + session['user_email'] + '/' + pic_name


    # save pic 
    product_pic.save(save_path)




    # define a product 
    p = {
        "owner":owner,
        "title":title, 
        "category":category, 
        "price":price, 
        "description":description,
        "post_date": post_date,
        "pic_path_for_html": path_for_html,  # save in user.py viewpoint
        "pic_path_for_app": save_path
    }

    # update db
    db.product.insert_one(p)

    # redirect to profile
    flash('Product Add!', category='success')

    return redirect(url_for('user.profile'))




@user.route('/profile/edit/<product_id>', methods=['POST', 'GET'])
def edit(product_id):

    # user object id to edit 
    object_id = ObjectId(product_id)
    p = db.product.find_one({"_id":object_id})

    if request.method == "POST":
        # get the request post
        title = request.form.get('product_title')
        category = request.form.get('product_category')
        price = request.form.get('product_price')
        description = request.form.get('product_description')

        # deifine a product 
        p_edit = {
            "title":title, 
            "category":category, 
            "price":price,
            "description":description
        }

        # update db
        db.product.update_one ({"_id":object_id}, {"$set": p_edit}, upsert=False)

        # redirect to profile
        flash('Product Edited!', category='success')
        return redirect(url_for('user.profile'))
        
    return render_template("edit_product.html", product = p)





@user.route('/profile/delete/<product_id>')
def delete(product_id):

    # use object id to remove one product from db.product
    object_id = ObjectId(product_id)
    # delete the pic
    p = db.product.find_one({"_id":object_id})
    try:
        os.remove(p['pic_path_for_app'])
        
    except:
        pass 

    # delete the db
    db.product.delete_one({"_id":object_id})
    
    flash('product delete!', category='success')

    return redirect(url_for('user.profile'))

