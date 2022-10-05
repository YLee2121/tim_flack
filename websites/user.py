from flask import Blueprint, render_template, redirect, url_for
user = Blueprint("user", __name__)

@user.route('/profile')
def profile():
    return redirect(url_for('auth.log_in'))
