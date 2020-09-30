#!/usr/bin/python3
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import mongo

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # first check if the user actually exists
    # take the inputted password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please try again, credentials seem to be wrong.')
        # if the user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.dashboard'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # Try to query the db to validate if user already exists, if it returns user than user exists.
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect them back to signup page so user can try again
        flash('It seems you are already a member')
        return redirect(url_for('auth.signup'))

    # create a new user with the form model db structure. Added password hash to prevent plaintext display.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    # adding the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/cancel')
@login_required
def cancel():
    if current_user is None:
        return redirect(url_for('index'))
    try:
        db.session.delete(current_user)
        db.session.commit()
    except:
        return 'unable to delete the user.'
    return render_template('cancel.html')

@auth.route('/addlog')
@login_required
def addlog():
    return render_template('addlog.html', log=mongo.db.log.find())

#@auth.route('/get_log')
#@login_required
#def get_log():
 #   return render_template('dashboard.html', log=mongo.db.log.find())
