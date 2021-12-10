# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.10 19:14
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @File : data2graph.py
# @Software : PyCharm

import graph as gp
from algorithm import *

dictionary = {
        "name": 0,
        "fee": 1,
        "location": 2,
        "qs2022_rank": 3,
        "qs2022_sequence": 4,
        "qs2021_rank" : 5,
        "qs2021_sequence" : 6,
        "qs2020_rank" : 7,
        "qs2020_sequence" : 8,
        "qs2019_rank" : 9,
        "qs2019_sequence" : 10,
        "usn2022_rank" : 11,
        "usn2022_sequence" : 12,
        "usnAH_rank" : 13,
        "usnAH_sequence" : 14,
        "usnBio_rank" : 15,
        "usnBio_sequence" : 16,
        "rate_graduation" : 17,
        "rate_acceptance" : 18,
        "rate_international" : 19,
        "rate_retention" : 20
    }

def graph_2D_XY_L(cur, x_name, y_name, title):
    cur.execute("select * from unv;")
    ax, ay, by = [], [], []
    for i in cur.fetchall():
        if i[dictionary[x_name]] is not None and i[dictionary[y_name]] is not None:
            if i[dictionary[x_name]] != 'NoneType' and i[dictionary[y_name]] != 'NoneType':
                ay.append(float(i[dictionary[x_name]]))
                by.append(float(i[dictionary[y_name]]))
    gp.itemXY_2D_L(figSize_wid_len=(10, 10), dpi=100, A_X=by, A_Y=ay, B_X=ay, B_Y=by, graph_title=title)

def expect(cur, x_name, y_name, rank_name, title):
    cur.execute("select * from unv;")
    p1, p2, pm = [], [], []
    pSum = 0.0
    count = 1
    for i in cur.fetchall():
        if i[dictionary[x_name]] is not None and i[dictionary[y_name]] is not None and i[dictionary[rank_name]] is not None:
            if i[dictionary[x_name]] != 'NoneType' and i[dictionary[y_name]] != 'NoneType' and i[dictionary[rank_name]] != 'NoneType':
                p1.append(float(i[dictionary[x_name]]))
                p2.append(float(i[dictionary[y_name]]))
                pSum += float(i[dictionary[x_name]]) * float(i[dictionary[y_name]]) * float(i[dictionary[rank_name]])
                count += 1
    print(str(title) + " is : " + str(pSum))

def graph_2D_XRankYRate(cur, rate1, rate2, rate3, names, title):
    cur.execute("select * from unv;")
    r1, r2, r3 = [], [], []
    for i in cur.fetchall():
        if i[dictionary[rate1]] is not None and i[dictionary[rate2]] is not None and i[dictionary[rate3]] is not None:
            if i[dictionary[rate1]] != 'NoneType' and i[dictionary[rate2]] != 'NoneType' and i[dictionary[rate3]] != 'NoneType':
                if i[dictionary[rate1]] != 0 and i[dictionary[rate2]] != 0 and i[dictionary[rate3]] != 0:
                    r1.append(float(i[dictionary[rate1]]))
                    r2.append(float(i[dictionary[rate2]]))
                    r3.append(float(i[dictionary[rate3]]))
    gp.itemXY_2D_XRankYRate(figSize_wid_len=(10, 10), dpi=100, Y=[r1, r2, r3], Y_lab=names, graph_title=title)

def graph_3D_GIF(cur, x_name, y_name, z_name, names, title):
    cur.execute("select * from unv;")
    x, y, z = [], [], []
    for i in cur.fetchall():
        if i[dictionary[x_name]] is not None and i[dictionary[y_name]] is not None and i[dictionary[z_name]] is not None:
            if i[dictionary[x_name]] != 'NoneType' and i[dictionary[y_name]] != 'NoneType' and i[dictionary[z_name]] != 'NoneType':
                if i[dictionary[x_name]] != 0 and i[dictionary[y_name]] != 0 and i[dictionary[z_name]] != 0:
                    x.append(float(i[dictionary[x_name]]))
                    y.append(float(i[dictionary[y_name]]))
                    z.append(float(i[dictionary[z_name]]))
    gp.itemXYZ_3D_GIF(".", figSize_wid_len=(10, 10), dpi=100, X=x, Y=y, Z=z, graph_title=title, x_name=names[0], y_name=names[1], z_name=names[2])

def exp_XY(cur, x_name, y_name):
    cur.execute("select * from unv;")
    x, y = [], []
    for i in cur.fetchall():
        if i[dictionary[x_name]] is not None and i[dictionary[y_name]] is not None:
            if i[dictionary[x_name]] != 'NoneType' and i[dictionary[y_name]] != 'NoneType':
                if i[dictionary[x_name]] != 0 and i[dictionary[y_name]] != 0:
                    x.append(float(i[dictionary[x_name]]))
                    y.append(float(i[dictionary[y_name]]))
    a, E = expected_value(x, y)
    if a:
        print(E)
    else:
        print(a)

