from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from . import db
from passlib.hash import pbkdf2_sha256

auth = Blueprint("auth", __name__)





@auth.route('/log_in', methods=["POST", "GET"])
def log_in():

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        u = db.user.find_one({"email": email})

        # email error
        if not u: 
            flash('Email has not signed up yet', category='error')

        # password error
        elif not pbkdf2_sha256.verify(password, u['password']): 
            flash('password incorrect', category='error')
        
        # log in successful
        else:
            return 'log in successful'


        

    return render_template('log_in.html')










@auth.route('/log_out')
def log_out():
    return render_template("log_out.html")








@auth.route('/sign_up', methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not email.endswith('@bu.edu'):
            flash('Email must end with @bu.edu', category='error')
        elif db.user.find_one({"email": email}):
            flash('Email in used', category='error')
        elif password1 != password2:
            flash('Password not the same', category='error')
        else:
            # create user object
            u = {
                "email":email, 
                "password":password1
                }

            # encrypt password
            u['password'] = pbkdf2_sha256.encrypt(u['password'])

            # insert into db 
            db.user.insert_one(u)

            flash('Account created!', category='success')

            return "sign in succ"




    return render_template("sign_up.html")

@auth.route("/testdb")
def testdb():
    u = {"email":"emailjdaiojfoas", "password":"passweorjaioew"}
    db.user.insert_one(u)
    db.product.insert_one(u)
    return "test"