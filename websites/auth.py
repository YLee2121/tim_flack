from email.message import EmailMessage
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from . import db, mail_server
from passlib.hash import pbkdf2_sha256
from .email_module import email_cls



auth = Blueprint("auth", __name__)


@auth.route('/log_in', methods=["POST", "GET"])
def log_in():

    if request.method == "POST":  
        
        # data from the html form
        email = request.form.get('email')
        password = request.form.get('password')

        # db search
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

    # if already logged in 
    if "logged" in session:
        return redirect(url_for('views.home'))


    return render_template('log_in.html')



@auth.route('/log_out')
def log_out():

    # if logged in
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


@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if request.method == "POST":
        
        email = request.form.get('email')

        # email not registered yet
        if not db.user.find_one({"email": email}):
            flash('Email not signed up yet!', category='error')
            # do here
        # email signed up already
        else:
            session['reset_email'] = email
            return render_template('reset_password_code.html')
    return render_template('reset_password.html')



@auth.route('/send')
def s():
    a = 'kylelee@gapp.nthu.edu.tw'
    code = email_cls.code_generator()
    msg = email_cls.create_mail_with_code(a, code)
    email_cls.send_mail(msg)
    return 'send'