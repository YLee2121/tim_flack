from flask import Blueprint, render_template, redirect, url_for, session
views = Blueprint("views", __name__)




@views.route("/")
def home():

    if "logged" in session:
        return render_template('home.html', email=session['user_email'])

    return redirect(url_for('auth.log_in'))






