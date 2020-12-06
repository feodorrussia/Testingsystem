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
    sub = Data.query.filter_by(name="subs").first().descr.split("; ")
    if request.method == 'GET':
        return render_template('index.html', faculties=faculties, col_edu=[1, 2, 3, 4, 5], subs=sub,
                               contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))
    elif request.method == 'POST':
        subs = []
        for i in sub:
            if request.form.get(f'{i}') != "":
                subs.append(int(request.form.get(f'{i}')))
            else:
                subs.append(0)
        sel_faculties = []
        for i in range(1, 6):
            f = request.form.get(f'faculties_{i}')
            if f in faculties:
                sel_faculties.append(f)
        if request.form.get('mode') == "manual" and sel_faculties != []:
            results = {}
            for sel_faculty in sel_faculties:
                if sel_faculty != "-":
                    fac = Faculties.query.filter_by(name=f'{sel_faculty}').first()
                    if fac and fac.id not in results.keys():
                        req_subs = fac.subjects.split()
                        result = 0
                        for i in req_subs:
                            result += subs[int(i)]
                        results[fac.id] = result
            req = Data(name="req", descr="; ".join([str(k) + " " + str(r) for k, r in results.items()]))
            db.session.add(req)
            db.session.commit()
            id_req = req.id
            return redirect(f"/result/{id_req}")
        else:
            result = sum(subs)
            return redirect(f"/result_rec/{result}")


@app.route('/result/<int:id_req>')
def result(id_req):
    sub = Data.query.filter_by(name="subs").first().descr.split("; ")
    req = Data.query.filter_by(id=f'{id_req}').first()
    result = sorted([list(map(int, x.split())) for x in req.descr.split("; ")], key=lambda x: -int(x[1]))
    return render_template('result.html', result=result, facts=Faculties(), sub=sub,
                           contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                               0].split("\n"))


@app.route('/result_rec/<int:result>')
def result_rec(result):  #
    faculties = [x.name for x in Faculties.query.all()]
    print(faculties)
    return render_template('result_rec.html', result=result, faculties=faculties, facts=Faculties(),
                           contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                               0].split(
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
