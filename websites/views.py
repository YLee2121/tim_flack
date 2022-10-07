from flask import Blueprint, render_template, redirect, url_for, session
from . import db

views = Blueprint("views", __name__)




@views.route("/")
def home():

    if "logged" not in session:
        return redirect(url_for('auth.log_in'))

    all_product = db.product.find({})
    print(all_product[0])
    
    return render_template("home.html", email=session['user_email'], all_product_online=all_product)




