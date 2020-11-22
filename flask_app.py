# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import redirect, render_template, request

from constants import *
from db import Admin
from db import Data
from db import Faculties
from little_functions import *
from login import LoginForm


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    faculties = [x.name for x in Faculties.query.all()]  #
    if request.method == 'GET':
        return render_template('index.html', faculties=faculties,
                               contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))
    elif request.method == 'POST':
        sel_faculties = request.form.get('faculties')
        subs = []
        for i in range(4):
            if request.form.get(f'{i}') != "":
                subs.append(int(request.form.get(f'{i}')))
            else:
                subs.append(0)
        req_subs = Faculties.query.filter_by(name=f'{sel_faculties}').first().subjects.split()
        result = 0
        for i in req_subs:
            result += subs[int(i)]
        return redirect(f"/result/{result}")


@app.route('/')
@app.route('/result/<int:result>')
def result(result):
    return render_template('result.html', result=result,
                           contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[0].split(
                               "\n"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    password = form.password.data
    if Admin.query.filter_by(password=password).all():
        Admin.query.filter_by(id=0).first().status = 1
        db.session.commit()
        return redirect("/ed_title")
    return render_template('loginform.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''
