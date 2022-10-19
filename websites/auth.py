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
        
        # already registered
        if db.user.find_one({"email": email}):
            flash('Email in used', category='error')

        #  # not bu mail
        # elif not email.endswith('@bu.edu'):
        #     flash('Email must end with @bu.edu', category='error')

        # password too short
        elif len(password1) < 6:
            flash('Passowrd too short (need to be longer than 6 characters)', category='error')
        
        # confirm password invalid
        elif password1 != password2:
            flash('Password not the same', category='error')
        
        # sign up success
        else:

            # encrypt password
            password1 = pbkdf2_sha256.encrypt(password1)
            
            # send verif code
            session['sign_up_email'] = email
            session['sign_up_password'] = password1
            return redirect(url_for('auth.send_code_sign_up'))
            
    return render_template("sign_up.html")

@auth.route('sign_up_code', methods=['GET', 'POST'])
def sign_up_code():

    if request.method == 'POST':

        verif_code = request.form.get('code')
        db_c = db.email_to_code.find_one({'email':session['sign_up_email']})
        db_code = db_c['code']

        if str(verif_code) != str(db_code):
            
            flash('Verification code incorrect', category='error')

        else:
            u = {
                "email":session['sign_up_email'],
                "password":session['sign_up_password']
            }
            db.user.insert_one(u)
            flash('Account created!', category='success')
            return redirect( url_for('auth.log_in'))

    return render_template('sign_up_code.html')





@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():

    if request.method == "POST":
        
        email = request.form.get('email')

        # email not registered yet
        if not db.user.find_one({"email": email}):
            flash('Email not signed up yet!', category='error')
        # email signed up already
        else:
            session['reset_email'] = email
            return redirect( url_for('auth.send_code_reset') )

    
    return render_template('reset_password.html')



@auth.route('/reset_password_code', methods=['GET', 'POST'])
def reset_password_code():
    
    # reset password process
    # verificatio code incorrect
    if request.method == "POST":
        new_password = request.form.get('password1')
        confirm_passowrd = request.form.get('password2')
        verif_code = request.form.get('code')

        db_c = db.email_to_code.find_one({'email':session['reset_email']})
        db_code = db_c['code']
        

        if str(verif_code) != str(db_code):
            
            flash('Verification code incorrect', category='error')

        # password too short
        elif len(new_password) < 6:
            flash('Passowrd too short (need to be longer than 6 characters)', category='error')
            
        # confirm password invalid
        elif new_password != confirm_passowrd:
            flash('Password not the same', category='error')

        # reset successfully
        else:
            # update user db
            data = {
                'password':pbkdf2_sha256.encrypt(new_password)
                }  
            query_filter = {'email': session['reset_email']}
            new_val = { "$set" : data}
            db.user.update_one(query_filter, new_val)

            flash('Reset password successfully', category='success')
            return redirect(url_for('auth.log_in'))

    return render_template('reset_password_code.html')



@auth.route('/send_code_sign_up')
def send_code_sign_up():
    # create code, send code, update db (email_to_code)
    sign_up_email = session['sign_up_email']
    email_cls.send_mail(sign_up_email)
    flash('Verification code sent!', category='success')
    return redirect( url_for('auth.sign_up_code'))

@auth.route('/send_code_reset')
def send_code_reset():
    # create code, send code, update db (email_to_code)
    reset_email = session['reset_email']
    email_cls.send_mail(reset_email)
    flash('Verification code sent!', category='success')
    return redirect( url_for('auth.reset_password_code'))
   


