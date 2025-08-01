from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def homepage():
    return render_template('home.html')

