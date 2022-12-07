from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy


from app import db, login_manager
from models import User

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/')
def index():
    return render_template('index.html')


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    remember = False
    if request.form.get('remember'):
        remember = True
    user = User.query.filter_by(email=request.form.get('email')).first()
    if not check_password_hash(user.password, request.form.get('password')):
        flash(user.password, 'error')
        return redirect(url_for('auth.login'))
    if not user or not check_password_hash(user.password, request.form.get('password')):
        flash('Wrong password or login', 'error')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.make_cv'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    pwd = request.form.get('password')
    if len(pwd) < 8:
        flash('Password is too short', 'error')
        return redirect(url_for('auth.signup'))
    if pwd != request.form.get('password_again'):
        flash('Password is not confirmed', 'error')
        return redirect(url_for('auth.signup'))
    if User.query.filter_by(email=email).first():
        flash('Email is already used', 'error')
        return redirect(url_for('auth.signup'))
    hash = generate_password_hash(pwd)
    new_user = User(email=email, name=request.form.get('name'),
                    password=hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main.make_cv'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out", "success")
    return redirect(url_for('auth.index'))
