# -*- coding = utf-8 -*-
# encoding: utf-8
# Python3.8

import os
import re
import sys
import time
import tkinter
from tkinter import filedialog
from bs4 import BeautifulSoup
from datetime import datetime
from fchooser import *
import sqlite3
from sqlite3 import Error
import graph as gp

def expected_value(X, P):
    if len(X) != len(P):
        return False, 0
    E = 0
    for i in range(len(X)):
        E += X[i] * P[i]
    return True, E


def readSQL(connect, cursor, sql_file_path):
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql = str(file.read())
            cursor.executescript(sql)
            connect.commit()
        return True
    except Exception as e:
        return e

def QS(connect, cursor, fileName : str = "", sqlKey1 : str = "", sqlKey2 : str = "", listRange : int = 100, error_count : int = 0):
    if fileName == "":
        fileName = fileChooser("Choose QS Ranking's HTML", [('HTML file', '*.html')])
    if sqlKey1 == "" or sqlKey2 == "":
        sqlKey1 = str(input("sql key 1 >>>"))
        sqlKey2 = str(input("sql key 2 >>>"))
    sqlKey = sqlKey1 + ", " + sqlKey2
    with open(fileName, 'r', encoding='utf-8') as file:
        file_html = file.read()
        uni_list = BeautifulSoup(file_html, 'html.parser').find_all("td", "uni")
        uni_rank_list = BeautifulSoup(file_html, 'html.parser').find_all("td", "rank")
        uni_sequence = 0
        count = listRange
        for i in range(listRange):
            count = count + 1
            print("\rUpdating " + fileName + ": " + str(count / 2) + " / " + str(listRange), end='')
            uni_sequence += 1
            uni_rank = str(BeautifulSoup(str(uni_rank_list[i]), 'html.parser').find("div", "td-wrap").get_text()).strip()
            uni_name = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uni_list[i]), 'html.parser').find("a", "uni-link").get_text()), count=0, flags=0)
            uni_name = re.sub(r' ".*"', '', uni_name, count=0, flags=0)
            uni_location = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uni_list[i]), 'html.parser').find("div", "location").get_text()).strip(), count=0, flags=0)
            uni_sql = 'INSERT INTO unv (name, location, fee, %s) VALUES ("%s", "%s", 0, "%s", %i);' % (sqlKey, uni_name, uni_location, uni_rank, uni_sequence)
            try:
                cursor.execute(uni_sql)
                connect.commit()
            except Exception:
                uni_sql = 'UPDATE unv SET (%s) = ("%s", %i) WHERE name = "%s";' % (sqlKey, uni_rank, uni_sequence, uni_name)
                try:
                    cursor.execute(uni_sql)
                    connect.commit()
                except Exception as exc:
                    error_count += 1
                    with open(r'.\error.log', 'a', encoding='utf-8') as log_file:
                        log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(exc) + "\n" + uni_sql + '\nInsert error (e003_' + fileName + ')\n\n')
    print("\n", end="")
    return error_count

def USN(connect, cursor, fileName : str = "", sqlKey1 : str = "", sqlKey2 : str = "", listRange : int = 100, error_count : int = 0):
    if fileName == "":
        fileName = fileChooser("Choose USNews Ranking's HTML", [('HTML file', '*.html')])
    if sqlKey1 == "" or sqlKey2 == "":
        sqlKey1 = str(input("sql key 1 >>>"))
        sqlKey2 = str(input("sql key 2 >>>"))
    sqlKey = sqlKey1 + ", " + sqlKey2
    with open(fileName, 'r', encoding='utf-8') as file:
        file_html = file.read()
        uni_list = BeautifulSoup(file_html, 'html.parser').find_all("section", "DetailCardGlobalUniversities__CardContainer-sc-1v60hm5-0 iEwxKW")
        fee_list = BeautifulSoup(file_html, 'html.parser').find_all("dd", "QuickStatHug__Description-hb1bl8-1 bBQBxy")
        uni_sequence = 0
        count = listRange
        for i in range(listRange):
            count = count + 1
            print("\rUpdating " + fileName + ": " + str(count / 2) + " / " + str(listRange), end='')
            uni_sequence += 1
            uni_name = str(BeautifulSoup(str(uni_list[i]), 'html.parser').find("a", "Anchor-byh49a-0 DetailCardGlobalUniversities__StyledAnchor-sc-1v60hm5-5 kQpddJ cTSURq").get_text())
            uni_name = re.sub(r' -- .*', '', uni_name, count=0, flags=0)
            uni_name = uni_name.replace("--", ", ")
            fee = str(fee_list[i * 2 - 1]).replace('<dd class="QuickStatHug__Description-hb1bl8-1 bBQBxy">', "").replace("</dd>", "")
            if "," in fee: fee = fee.replace(",", "").strip()
            else: fee = "0"
            try: uni_rank = str(BeautifulSoup(str(uni_list[i]), 'html.parser').find("strong").get_text())
            except Exception: uni_rank = "-1"
            try: uni_location = str(BeautifulSoup(str(uni_list[i]), 'html.parser').find("span").get_text())
            except Exception: uni_location = "?"
            uni_sql = 'INSERT INTO unv (name, location, fee, %s) VALUES ("%s", "%s", %s, "%s", %i);' % (sqlKey, uni_name, uni_location, fee, uni_rank, uni_sequence)
            try:
                cursor.execute(uni_sql)
                connect.commit()
            except Exception:
                uni_sql = 'UPDATE unv SET (%s) = ("%s", %i) WHERE name = "%s";' % (sqlKey, uni_rank, uni_sequence, uni_name)
                try:
                    cursor.execute(uni_sql)
                    connect.commit()
                except Exception as exc:
                    error_count += 1
                    with open(r'.\error.log', 'a', encoding='utf-8') as log_file:
                        log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(exc) + "\n" + uni_sql + '\nInsert error (e003_' + fileName + ')\n\n')
    print("\n", end="")
    return error_count

def USNRate(connect, cursor, fileName : str = "", sqlKey : str = "", error_count : int = 0):
    if fileName == "":
        fileName = fileChooser("Choose USNews Ranking's HTML", [('HTML file', '*.html')])
    with open(fileName, 'r', encoding='utf-8') as file:
        file_html = file.read()
        uni_list = BeautifulSoup(file_html, 'html.parser').find_all("tr")
        count = 0
        for i in uni_list:
            count = count + 1
            print("\rUpdating " + fileName + ": " + str(count) + " / " + str(len(uni_list)), end='')
            try:
                uni_rate = float(str(BeautifulSoup(str(i), 'html.parser').find_all("span", "Span-sc-19wk4id-0 frTdxR")[2].get_text()).replace("%", "")) / 100.0
                uni_name = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(i), 'html.parser').find("a", "Anchor-byh49a-0 kQpddJ").get_text()), count=0, flags=0)
                uni_name = re.sub(r' -- .*', '', uni_name, count=0, flags=0)
                uni_name = uni_name.replace("--", ", ")
                uni_sql = 'INSERT INTO unv (name, %s) VALUES ("%s", %f);' % (sqlKey, uni_name, uni_rate)
                cursor.execute(uni_sql)
                connect.commit()
            except Exception:
                try:
                    uni_sql = 'UPDATE unv SET %s = %f WHERE name = "%s";' % (sqlKey, uni_rate, uni_name)
                    cursor.execute(uni_sql)
                    connect.commit()
                except Exception as exc:
                    error_count += 1
                    with open(r'.\error.log', 'a', encoding='utf-8') as log_file:
                        log_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(exc) + "\n" + uni_sql + '\nInsert error (e003_' + fileName + ')\n\n')
    print("\n", end="")
    return error_count

def graph_2D_XY_L(x_name, y_name, title):
    name_i = {
        "name": 0,
        "fee": 1,
        "location": 2,
        "qs2022_rank": 3,
        "qs2022_sequence": 4,
        "qs2021_rank": 5,
        "qs2021_sequence": 6,
        "qs2020_rank": 7,
        "qs2020_sequence": 8,
        "qs2019_rank": 9,
        "qs2019_sequence": 10,
        "usn2022_rank": 11,
        "usn2022_sequence": 12,
        "usnAH_rank": 13,
        "usnAH_sequence": 14,
        "usnBio_rank": 15,
        "usnBio_sequence": 16,
        "rate_graduation": 17,
        "rate_acceptance": 18,
        "rate_international": 19,
        "rate_retention": 20
    }
    cur.execute("select * from unv;")
    ax, ay, by = [], [], []
    for i in cur.fetchall():
        if i[name_i[x_name]] is not None and i[name_i[y_name]] is not None:
            if i[name_i[x_name]] != 'NoneType' and i[name_i[y_name]] != 'NoneType':
                ay.append(float(i[name_i[x_name]]))
                by.append(float(i[name_i[y_name]]))
    gp.itemXY_2D_L(figSize_wid_len=(10, 10), dpi=100, A_X=by, A_Y=ay, B_X=ay, B_Y=by, graph_title=title)

def expect(x_name, y_name, rank_name, title):
    name_i = {
        "name": 0,
        "fee": 1,
        "location": 2,
        "qs2022_rank": 3,
        "qs2022_sequence": 4,
        "qs2021_rank": 5,
        "qs2021_sequence": 6,
        "qs2020_rank": 7,
        "qs2020_sequence": 8,
        "qs2019_rank": 9,
        "qs2019_sequence": 10,
        "usn2022_rank": 11,
        "usn2022_sequence": 12,
        "usnAH_rank": 13,
        "usnAH_sequence": 14,
        "usnBio_rank": 15,
        "usnBio_sequence": 16,
        "rate_graduation": 17,
        "rate_acceptance": 18,
        "rate_international": 19,
        "rate_retention": 20,
        "1": 1,
        "0": 0
    }
    cur.execute("select * from unv;")
    p1, p2, pm = [], [], []
    pSum = 0.0
    count = 1
    for i in cur.fetchall():
        if i[name_i[x_name]] is not None and i[name_i[y_name]] is not None and i[name_i[rank_name]] is not None:
            if i[name_i[x_name]] != 'NoneType' and i[name_i[y_name]] != 'NoneType' and i[name_i[rank_name]] != 'NoneType':
                p1.append(float(i[name_i[x_name]]))
                p2.append(float(i[name_i[y_name]]))
                pSum += float(i[name_i[x_name]])*float(i[name_i[y_name]])*float(i[name_i[rank_name]])
                count += 1
    print(str(title) + " is : " + str(pSum))

def graph_2D_XRankYRate(rate1, rate2, rate3, names, title):
    name_i = {
        "name": 0,
        "fee": 1,
        "location": 2,
        "qs2022_rank": 3,
        "qs2022_sequence": 4,
        "qs2021_rank": 5,
        "qs2021_sequence": 6,
        "qs2020_rank": 7,
        "qs2020_sequence": 8,
        "qs2019_rank": 9,
        "qs2019_sequence": 10,
        "usn2022_rank": 11,
        "usn2022_sequence": 12,
        "usnAH_rank": 13,
        "usnAH_sequence": 14,
        "usnBio_rank": 15,
        "usnBio_sequence": 16,
        "rate_graduation": 17,
        "rate_acceptance": 18,
        "rate_international": 19,
        "rate_retention": 20
    }
    cur.execute("select * from unv;")
    r1, r2, r3 = [], [], []
    for i in cur.fetchall():
        if i[name_i[rate1]] is not None and i[name_i[rate2]] is not None and i[name_i[rate3]] is not None:
            if i[name_i[rate1]] != 'NoneType' and i[name_i[rate2]] != 'NoneType' and i[name_i[rate3]] != 'NoneType':
                if i[name_i[rate1]] != 0 and i[name_i[rate2]] != 0 and i[name_i[rate3]] != 0:
                    r1.append(float(i[name_i[rate1]]))
                    r2.append(float(i[name_i[rate2]]))
                    r3.append(float(i[name_i[rate3]]))
    gp.itemXY_2D_XRankYRate(figSize_wid_len=(10, 10), dpi=100, Y=[r1, r2, r3], Y_lab=names, graph_title=title)

def graph_3D_GIF(x_name, y_name, z_name, names, title):
    name_i = {
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
    cur.execute("select * from unv;")
    x, y, z = [], [], []
    for i in cur.fetchall():
        if i[name_i[x_name]] is not None and i[name_i[y_name]] is not None and i[name_i[z_name]] is not None:
            if i[name_i[x_name]] != 'NoneType' and i[name_i[y_name]] != 'NoneType' and i[name_i[z_name]] != 'NoneType':
                if i[name_i[x_name]] != 0 and i[name_i[y_name]] != 0 and i[name_i[z_name]] != 0:
                    x.append(float(i[name_i[x_name]]))
                    y.append(float(i[name_i[y_name]]))
                    z.append(float(i[name_i[z_name]]))
    gp.itemXYZ_3D_GIF(".", figSize_wid_len=(10, 10), dpi=100, X=x, Y=y, Z=z, graph_title=title, x_name=names[0], y_name=names[1], z_name=names[2])

def exp_XY(x_name, y_name):
    name_i = {
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
    cur.execute("select * from unv;")
    x, y = [], []
    for i in cur.fetchall():
        if i[name_i[x_name]] is not None and i[name_i[y_name]] is not None:
            if i[name_i[x_name]] != 'NoneType' and i[name_i[y_name]] != 'NoneType':
                if i[name_i[x_name]] != 0 and i[name_i[y_name]] != 0:
                    x.append(float(i[name_i[x_name]]))
                    y.append(float(i[name_i[y_name]]))
    a, E = expected_value(x, y)
    if a:
        print(E)
    else:
        print(a)


if __name__ == '__main__':
    print("Initializing...")
    # 初始化Tk
    tkinter.Tk().withdraw()
    time_value = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    # con = sqlite3.connect(time_value + ".db")
    con = sqlite3.connect("2021-12-06_17-49-10.db")
    cur = con.cursor()
    # if readSQL(con, cur, "./db_initialize.sql") is True:
    if True:
        try:
            print("Converting...")
            time_start = time.time()
            error = 0
            # #############################################################################################################################################################
            # error = USN(connect=con, cursor=cur, fileName="USNews_2022.html", sqlKey1="usn2022_rank", sqlKey2="usn2022_sequence", listRange=1190, error_count=error)
            # error = USN(connect=con, cursor=cur, fileName="USNews_A&H.html", sqlKey1="usnAH_rank", sqlKey2="usnAH_sequence", listRange=250, error_count=error)
            # error = USN(connect=con, cursor=cur, fileName="USNews_Bio.html", sqlKey1="usnBio_rank", sqlKey2="usnBio_sequence", listRange=500, error_count=error)
            # error = QS(connect=con, cursor=cur, fileName="QS_2022.html", sqlKey1="qs2022_rank", sqlKey2="qs2022_sequence", listRange=1200, error_count=error)
            # error = QS(connect=con, cursor=cur, fileName="QS_2021.html", sqlKey1="qs2021_rank", sqlKey2="qs2021_sequence", listRange=1000, error_count=error)
            # error = QS(connect=con, cursor=cur, fileName="QS_2020.html", sqlKey1="qs2020_rank", sqlKey2="qs2020_sequence", listRange=1000, error_count=error)
            # error = QS(connect=con, cursor=cur, fileName="QS_2019.html", sqlKey1="qs2019_rank", sqlKey2="qs2019_sequence", listRange=1000, error_count=error)
            # error = USNRate(connect=con, cursor=cur, fileName="Rates_Graduation.html", sqlKey="rate_graduation", error_count=error)
            # error = USNRate(connect=con, cursor=cur, fileName="Rates_Acceptance1.html", sqlKey="rate_acceptance", error_count=error)
            # error = USNRate(connect=con, cursor=cur, fileName="Rates_Acceptance2.html", sqlKey="rate_acceptance", error_count=error)
            # error = USNRate(connect=con, cursor=cur, fileName="Rates_International.html", sqlKey="rate_international", error_count=error)
            # error = USNRate(connect=con, cursor=cur, fileName="Rates_Retention.html", sqlKey="rate_retention", error_count=error)
            # graph_3D_GIF("usn2022_sequence", "qs2022_sequence", "rate_graduation", ["USNews Rank 2022", "QS Rank 2022", "Graduation Rate"], "QS/USNews Graduation Rate")
            # graph_3D_GIF("rate_acceptance", "rate_graduation", "usn2022_sequence", ["Acceptance Rate", "Graduation Rate", "USNews Rank 2022"], "Acceptance/Graduation Rate (USNews)")
            # graph_3D_GIF("rate_acceptance", "rate_graduation", "qs2022_sequence", ["Acceptance Rate", "Graduation Rate", "QS Rank 2022"], "Acceptance/Graduation Rate (QS)")
            # # graph_3D_GIF("qs2022_sequence", "qs2021_sequence", "qs2020_sequence", ["QS Rank 2022", "QS Rank 2021", "QS Rank 2020"], "QS 2022-2020")
            # graph_3D_GIF("rate_acceptance", "rate_graduation", "rate_international", ["Acceptance Rate", "Graduation Rate", "International Rate"], "Acceptance/Graduation/International Rate")
            # graph_3D_GIF("usn2022_sequence", "qs2022_sequence", "fee", ["USNews Rank 2022", "QS Rank 2022", "Expenses"], "QS/USNews/Expenses")
            # graph_2D_XY_L("usn2022_sequence", "qs2022_sequence", "QS/USNews 2022")
            # graph_2D_XRankYRate("rate_acceptance", "rate_graduation", "rate_international", ["Acceptance Rate", "Graduation Rate", "International Rate"], "Acceptance/Graduation/International Rate")
            # graph_2D_XRankYRate("rate_acceptance", "rate_graduation", "rate_retention", ["Acceptance Rate", "Graduation Rate", "Retention Rate"], "Acceptance/Graduation/Retention Rate")
            # exp_XY("usn2022_sequence", "rate_acceptance")
            # expect("rate_acceptance", "rate_graduation", "qs2022_sequence", "Expected Value (X=QS_2022_Rank, P=p(Acceptance Rate)*p(Graduation Rate))")
            # expect("rate_acceptance", "rate_graduation", "qs2021_sequence", "Expected Value (X=QS_2021_Rank, P=p(Acceptance Rate)*p(Graduation Rate))")
            # expect("rate_acceptance", "rate_graduation", "qs2020_sequence", "Expected Value (X=QS_2020_Rank, P=p(Acceptance Rate)*p(Graduation Rate))")
            # expect("rate_acceptance", "rate_graduation", "qs2019_sequence", "Expected Value (X=QS_2019_Rank, P=p(Acceptance Rate)*p(Graduation Rate))")
            # expect("rate_acceptance", "rate_graduation", "usn2022_sequence", "Expected Value (X=USNews_2019_Rank, P=p(Acceptance Rate)*p(Graduation Rate))")
            # expect("rate_international", "rate_graduation", "qs2022_sequence", "Expected Value (X=QS_2022_Rank, P=p(International Rate)*p(Graduation Rate))")
            # expect("rate_international", "rate_graduation", "qs2021_sequence", "Expected Value (X=QS_2021_Rank, P=p(International Rate)*p(Graduation Rate))")
            # expect("rate_international", "rate_graduation", "qs2020_sequence", "Expected Value (X=QS_2020_Rank, P=p(International Rate)*p(Graduation Rate))")
            # expect("rate_international", "rate_graduation", "qs2019_sequence", "Expected Value (X=QS_2019_Rank, P=p(International Rate)*p(Graduation Rate))")
            # expect("rate_international", "rate_graduation", "usn2022_sequence", "Expected Value (X=USNews_2019_Rank, P=p(International Rate)*p(Graduation Rate))")
            # #############################################################################################################################################################
            time_end = time.time()
            timeCost = time_end - time_start
            timeUnit = "s"
            if timeCost >= 60:
                timeCost = timeCost / 60
                timeUnit = "m"
            print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(timeCost), 3)) + timeUnit)
            cur.close()
            con.close()
        except FileNotFoundError as te:
            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n\n')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n\n')
        except Exception as e:
            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n\n')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n\n')


