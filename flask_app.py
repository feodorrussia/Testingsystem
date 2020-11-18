# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import redirect, render_template, request

from constants import *
from db import Admin
from db import Data
from little_functions import *
from login import LoginForm


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    edu_org = ["physical and mathematical profile", "information and mathematical profile"]  #
    if request.method == 'GET':
        return render_template('index.html', edu_org=edu_org,
                               contacts=information_extractor(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))
    elif request.method == 'POST':
        sel_edu_org = request.form.get('edu_org')
        subs = []
        for i in range(4):
            subs.append(int(request.form.get(f'{i}')))
        if sel_edu_org == edu_org[0]:  #
            result = (subs[0] + subs[1] + subs[2]) // 3
        elif sel_edu_org == edu_org[1]:  #
            result = (subs[0] + subs[1] + subs[3]) // 3
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
