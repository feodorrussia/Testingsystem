from constants import *


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=True, nullable=False, default='123467890')
    status = db.Column(db.Integer, unique=False, nullable=False, default='0')


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    descr = db.Column(db.String(1200), unique=False, nullable=True)


class Faculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), unique=True, nullable=False)
    id_uni = db.Column(db.Integer, unique=False, nullable=False)
    subjects = db.Column(db.String(80), unique=False, nullable=False)
    passing_score = db.Column(db.Integer, unique=False, nullable=False)


class Universities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)


class Individual_achivements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    descr = db.Column(db.String(1280), unique=False, nullable=True)


class University_Ach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_uni = db.Column(db.Integer, unique=False, nullable=False)
    id_ach = db.Column(db.Integer, unique=False, nullable=False)
    point = db.Column(db.Integer, unique=False, nullable=False)
    descr = db.Column(db.String(320), unique=False, nullable=True)


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)


class University_Sub(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_uni = db.Column(db.Integer, unique=False, nullable=False)
    id_sub = db.Column(db.Integer, unique=False, nullable=False)
    limit_score = db.Column(db.Integer, unique=False, nullable=False)

class Sub_Comb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_fac = db.Column(db.Integer, unique=False, nullable=False)
    subs = db.Column(db.String(80), unique=False, nullable=False)
    user = db.Column(db.Integer, unique=False, nullable=False)
    fl = db.Column(db.Integer, unique=False, nullable=False)


db.create_all()
