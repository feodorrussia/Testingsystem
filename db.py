from constants import *


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=True, nullable=False, default='123467890')
    status = db.Column(db.Integer, unique=False, nullable=False, default='0')


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    descr = db.Column(db.String(80), unique=False, nullable=False)



class Universities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    add_score = db.Column(db.String(80), unique=True, nullable=False)


class Faculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    university = db.Column(db.String(80), unique=False, nullable=False)
    subjects = db.Column(db.String(80), unique=False, nullable=False)
    passing_score = db.Column(db.Integer, unique=False, nullable=False)

db.create_all()
