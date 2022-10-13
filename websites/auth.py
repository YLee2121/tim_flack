from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from . import db, EMAIL_SERVER
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
            session['logged'] = True  
            session['user_email'] = email   
            flash('Log in successfully', category='success')
            return redirect(url_for('views.home'))

    if "logged" in session:
        return redirect(url_for('views.home'))


    return render_template('log_in.html')



@auth.route('/log_out')
def log_out():
    if "logged" in session:
        session.clear()
        flash('Log out successful', category='success')
        return redirect(url_for('auth.log_in'))
    
    return redirect(url_for('auth.log_in'))



@auth.route('/sign_up', methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(type(password1), len(password1))

        # not bu mail
        if not email.endswith('@bu.edu'):
            flash('Email must end with @bu.edu', category='error')
        
        # already registered
        elif db.user.find_one({"email": email}):
            flash('Email in used', category='error')

        # password too short
        elif len(password1) < 6:
            flash('Passowrd too short (need to be longer than 6 characters)', category='error')
        
        # confirm password invalid
        elif password1 != password2:
            flash('Password not the same', category='error')
        
        # sign up success
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

            return redirect(url_for('auth.log_in'))
            
    return render_template("sign_up.html")


@auth.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')