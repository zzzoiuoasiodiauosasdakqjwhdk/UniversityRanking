# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.10 19:10
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @File : html2data.py
# @Software : PyCharm

import re
import time
from bs4 import BeautifulSoup

def QS(connect, cursor, fileName: str, sqlKey1: str, sqlKey2: str, error_count: int = 0):
    keyList = []
    for i in cursor.execute("PRAGMA table_info('unv')").fetchall():
        keyList.append(i[1])
    try:
        if sqlKey1 not in keyList:
            sql = "ALTER TABLE unv ADD COLUMN %s TEXT;" % sqlKey1
            cursor.execute(sql)
            connect.commit()
        if sqlKey2 not in keyList:
            sql = "ALTER TABLE unv ADD COLUMN %s INTEGER;" % sqlKey2
            cursor.execute(sql)
            connect.commit()
    except Exception:
        return -8800
    sqlKey = sqlKey1 + ", " + sqlKey2
    with open(fileName, 'r', encoding='utf-8') as file:
        file_html = file.read()
        uni_list = BeautifulSoup(file_html, 'html.parser').find_all("td", "uni")
        uni_rank_list = BeautifulSoup(file_html, 'html.parser').find_all("td", "rank")
        uni_sequence = 0
        count = len(uni_list)
        for i in range(len(uni_list)):
            count = count + 1
            print("\rUpdating " + fileName + ": " + str(count / 2) + " / " + str(len(uni_list)), end='')
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


def USN(connect, cursor, fileName: str, sqlKey1: str, sqlKey2: str, error_count: int = 0):
    keyList = []
    for i in cursor.execute("PRAGMA table_info('unv')").fetchall():
        keyList.append(i[1])
    try:
        if sqlKey1 not in keyList:
            sql = "ALTER TABLE unv ADD COLUMN %s TEXT;" % sqlKey1
            cursor.execute(sql)
            connect.commit()
        if sqlKey2 not in keyList:
            sql = "ALTER TABLE unv ADD COLUMN %s INTEGER;" % sqlKey2
            cursor.execute(sql)
            connect.commit()
    except Exception:
        return -8800
    sqlKey = sqlKey1 + ", " + sqlKey2
    with open(fileName, 'r', encoding='utf-8') as file:
        file_html = file.read()
        uni_list = BeautifulSoup(file_html, 'html.parser').find_all("section", "DetailCardGlobalUniversities__CardContainer-sc-1v60hm5-0 iEwxKW")
        fee_list = BeautifulSoup(file_html, 'html.parser').find_all("dd", "QuickStatHug__Description-hb1bl8-1 bBQBxy")
        uni_sequence = 0
        count = len(uni_list)
        for i in range(len(uni_list)):
            count = count + 1
            print("\rUpdating " + fileName + ": " + str(count / 2) + " / " + str(len(uni_list)), end='')
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


def USNRate(connect, cursor, fileName: str, sqlKey: str, error_count: int = 0):
    keyList = []
    for i in cursor.execute("PRAGMA table_info('unv')").fetchall():
        keyList.append(i[1])
    try:
        if sqlKey not in keyList:
            sql = "ALTER TABLE unv ADD COLUMN %s FLOAT;" % sqlKey
            cursor.execute(sql)
            connect.commit()
    except Exception:
        return -8800
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
