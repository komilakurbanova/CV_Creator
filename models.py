from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    password_again = db.Column(db.String(100), unique=True, nullable=False)


class CV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    skills = db.Column(db.String(1200))
    education = db.Column(db.String(1200))
    job_exp = db.Column(db.String(1200))
    image = db.Column(db.BLOB)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('CVs', lazy=True))
