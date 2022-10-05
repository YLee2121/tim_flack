
from flask import Blueprint, render_template, redirect, url_for, session
user = Blueprint("user", __name__)

@user.route('/profile')
def profile():

    if "logged" not in session:
        return redirect(url_for('auth.log_in'))

    return render_template('profile.html', email=session['user_email'])