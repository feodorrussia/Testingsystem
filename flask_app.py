# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import redirect, render_template, request

from constants import *
from db import Admin
from db import Data
from db import Faculties
from db import Individual_achivements
from db import Sub_Comb
from db import Universities as Uni
from db import University_Ach
from db import University_Sub
from little_functions import *
from login import LoginForm


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    faculties = [x.name for x in Faculties.query.all()]  #
    sub = Data.query.filter_by(name="subs").first().descr.split("; ")[1:]
    if request.method == 'GET':
        return render_template('index.html', faculties=faculties, col_edu=range(1, 8), subs=sub,
                               help_text=information_extractor_f("help.txt")[0].split("\n"),
                               contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))
    elif request.method == 'POST':
        global sub_combs
        req = Data(name="req", descr="")
        db.session.add(req)
        db.session.commit()
        id_req = req.id
        subs = [0]
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
                    fl = False
                    if fac and fac.id not in results.keys():
                        req_subs = fac.subjects.split()
                        result = 0
                        flag = 1
                        for i in req_subs:
                            ege_score = subs[int(i)]
                            limit_score = University_Sub.query.filter_by(id_uni=fac.id_uni).filter_by(
                                id_sub=i).first().limit_score
                            if limit_score <= ege_score:
                                score = f"g{sub[int(i) - 1][0]}"
                            else:
                                score = f"r{sub[int(i) - 1][0]}"
                                flag = 0
                            sub_comb = Sub_Comb.query.filter_by(id_fac=fac.id).filter_by(
                                subs=fac.subjects).filter_by(user=id_req).first()
                            if not sub_comb:
                                sub_comb_n = Sub_Comb(id_fac=fac.id, subs=fac.subjects, fl=flag, user=id_req)
                                db.session.add(sub_comb_n)
                                db.session.commit()
                                sub_combs[sub_comb_n.id] = [score]
                            else:
                                db.session.query(Sub_Comb).filter_by(id_fac=fac.id).filter_by(
                                    subs=fac.subjects).filter_by(user=id_req).update({"fl": flag})
                                db.session.commit()
                                sub_combs[sub_comb.id].append(score)
                            result += ege_score
                        results[fac.id] = [str(result)]
            fl = "0"
            if request.form.get('mode_achieve') == "ind_achieve":
                fl = "1"
                individual_achievements = [x.strip().lower() for x in request.form.get('ind_achieve').split("\n")]
                for fac_id in results.keys():
                    if len(results[fac_id]) == 1:
                        results[fac_id].append("0")
                    uni = Faculties.query.filter_by(id=fac_id).first().id_uni
                    print(sorted(University_Ach.query.filter_by(id_uni=uni).all(), key=lambda x: -x.point))
                    for ind_ach in sorted(University_Ach.query.filter_by(id_uni=uni).all(), key=lambda x: -x.point):
                        id_ach, point = ind_ach.id_ach, ind_ach.point
                        ach = Individual_achivements.query.filter_by(id=id_ach).first().name
                        if ach.lower() in individual_achievements:
                            if int(results[fac_id][1]) + int(point) <= 10:
                                results[fac_id][1] = str(int(results[fac_id][1]) + int(point))
                            else:
                                results[fac_id][1] = str(max(int(results[fac_id][1]), int(point)))
                            results[fac_id].append(str(id_ach))
        else:
            results = {}
            for fac in Faculties.query.all():
                fl = False
                if fac and fac.id not in results.keys():
                    req_subs = fac.subjects.split()
                    result = 0
                    flag = 1
                    for i in req_subs:
                        ege_score = subs[int(i)]
                        limit_score = University_Sub.query.filter_by(id_uni=fac.id_uni).filter_by(
                            id_sub=i).first().limit_score
                        if limit_score <= ege_score:
                            score = f"g{sub[int(i) - 1][0]}"
                        else:
                            score = f"r{sub[int(i) - 1][0]}"
                            flag = 1
                        sub_comb = Sub_Comb.query.filter_by(id_fac=fac.id).filter_by(
                            sub=fac.subjects).filter_by(user=id_req).first()
                        if not sub_comb:
                            sub_comb_n = Sub_Comb(id_fac=fac.id, subs=fac.subjects, fl=flag, user=id_req)
                            db.session.add(sub_comb_n)
                            db.session.commit()
                            sub_combs[sub_comb_n.id] = [score]
                            fl = True
                        elif fl:
                            db.session.query(Sub_Comb).filter_by(id_fac=fac.id).filter_by(
                                subs=fac.subjects).filter_by(user=id_req).update({"fl": flag})
                            db.session.commit()
                            sub_combs[sub_comb.id].append(score)
                        result += ege_score
                    results[fac.id] = [str(result)]
            fl = "0"
            if request.form.get('mode_achieve') == "ind_achieve":
                fl = "1"
                individual_achievements = [x.strip().lower() for x in request.form.get('ind_achieve').split("\n")]
                for fac_id in results.keys():
                    if len(results[fac_id]) == 1:
                        results[fac_id].append("0")
                    uni = Faculties.query.filter_by(id=fac_id).first().id_uni
                    for ind_ach in sorted(University_Ach.query.filter_by(id_uni=uni).all(), key=lambda x: -x.point):
                        id_ach, score = ind_ach.id_ach, ind_ach.point
                        ach = Individual_achivements.query.filter_by(id=id_ach).first().name
                        if ach.lower() in individual_achievements:
                            if int(results[fac_id][1]) + int(score) <= 10:
                                results[fac_id][1] = str(int(results[fac_id][1]) + int(score))
                            else:
                                results[fac_id][1] = str(max(int(results[fac_id][1]), int(score)))
                            results[fac_id].append(str(id_ach))
        req = db.session.query(Data).get(id_req)
        req.descr = fl + "; ".join([str(k) + " " + " ".join(r) for k, r in results.items()])
        db.session.commit()
        return redirect(f"/result/{id_req}")


@app.route('/result/<int:id_req>')
def result(id_req):
    global sub_combs
    sub = Data.query.filter_by(name="subs").first().descr.split("; ")
    req = Data.query.filter_by(id=f'{id_req}').first().descr
    uni = [x.name for x in Uni.query.all()]
    if req[0] == "1":
        result = sorted([list(map(int, i.split())) for i in req[1:].split("; ")], key=lambda x: -int(x[1]))
        print(result)
        return render_template('result_wia.html', result=result, facts=Faculties(), sub=sub, uni=uni,
                               sub_comb=Sub_Comb(), id_req=id_req, sub_combs=sub_combs,
                               ind_ach=Individual_achivements(), uni_ach=University_Ach(), uni_sub=University_Sub(),
                               contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))
    else:
        result = sorted([list(map(int, x.split())) for x in req[1:].split("; ")], key=lambda x: -int(x[1]))
        print(result)  # [Faculties.query.filter_by(id=5).first().subjects][1]
        return render_template('result_na.html', result=result, facts=Faculties(), sub=sub, uni=uni,
                               sub_comb=Sub_Comb(), id_req=id_req, sub_combs=sub_combs,
                               contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    password = form.password.data
    if Admin.query.filter_by(password=password).all():
        Admin.query.filter_by(id=0).first().status = 1
        db.session.commit()
        return redirect("/ed_title")
    return render_template('loginform.html', form=form)


@app.route('/help')
def help():
    return render_template('help.html', text=information_extractor_f("help.txt")[0].split("\n"),
                               contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))


@app.route('/about_us')
def about_us():
    return render_template('about_us.html', text=information_extractor_f("help.txt")[0].split("\n"),
                               contacts=information_extractor_f(Data.query.filter_by(name="contacts").first().descr)[
                                   0].split("\n"))


if __name__ == '__main__':
    app.run(debug=True)
'''port=8080, host='127.0.0.1'''
