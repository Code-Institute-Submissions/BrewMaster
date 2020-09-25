#!/usr/bin/python3
import os
from flask import Blueprint, render_template, current_user
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

if __name__ == '__main__':
    main.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)