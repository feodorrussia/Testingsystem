from constants import *


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), unique=True, nullable=False, default='123467890')
    status = db.Column(db.Integer, unique=False, nullable=False, default='0')


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(80), unique=True, nullable=False)
    filename = db.Column(db.String(80), unique=False, nullable=False)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    descr = db.Column(db.String(80), unique=False, nullable=False)

class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=False, nullable=False)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_filename = db.Column(db.String(80), unique=False, nullable=False)
    image_filename = db.Column(db.String(80), unique=False, nullable=False)


db.create_all()
