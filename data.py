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
from database import *

if __name__ == '__main__':
    print("Initializing...")
    # 初始化Tk
    tkinter.Tk().withdraw()
    tryDB, con, cur = db(str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())) + ".db")
    if tryDB is True:
        try:
            with open("USNews_2022.html", 'r', encoding='utf-8') as html_file:
                print("Converting...")
                html = html_file.read()
                uniList = BeautifulSoup(html, 'html.parser').find_all("section", "DetailCardGlobalUniversities__CardContainer-sc-1v60hm5-0 iEwxKW")
                feeList = BeautifulSoup(html, 'html.parser').find_all("dd", "QuickStatHug__Description-hb1bl8-1 bBQBxy")
                sequence = 0
                for i in range(1190):
                    sequence += 1
                    name = str(BeautifulSoup(str(uniList[i]), 'html.parser').find("a", "Anchor-byh49a-0 DetailCardGlobalUniversities__StyledAnchor-sc-1v60hm5-5 kQpddJ cTSURq").get_text())
                    name = re.sub(r' -- .*', '', name, count=0, flags=0)
                    name = name.replace("--", ", ")
                    fee = str(feeList[i*2-1]).replace('<dd class="QuickStatHug__Description-hb1bl8-1 bBQBxy">', "").replace("</dd>", "")
                    if "," in fee:
                        fee = fee.replace(",", "").strip()
                    else:
                        fee = "0"
                    try: rank = str(BeautifulSoup(str(uniList[i]), 'html.parser').find("strong").get_text())
                    except Exception: rank = "?"
                    try: location = str(BeautifulSoup(str(uniList[i]), 'html.parser').find("span").get_text())
                    except Exception: location = "?"
                    sql = 'INSERT INTO unv (name, location, fee, usn2022_rank, usn2022_sequence) VALUES ("%s", "%s", %s, "%s", %i);' % (name, location, fee, rank, sequence)
                    try:
                        cur.execute(sql)
                        con.commit()
                    except Exception as e:
                        with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                            error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_USNews_2022.html)\n\n')
                        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_USNews_2022.html)\n\n')
            with open("USNews_A&H.html", 'r', encoding='utf-8') as html_file:
                print("Converting...")
                html = html_file.read()
                uniList = BeautifulSoup(html, 'html.parser').find_all("section", "DetailCardGlobalUniversities__CardContainer-sc-1v60hm5-0 iEwxKW")
                sequence = 0
                for i in range(250):
                    sequence += 1
                    name = str(BeautifulSoup(str(uniList[i]), 'html.parser').find("a", "Anchor-byh49a-0 DetailCardGlobalUniversities__StyledAnchor-sc-1v60hm5-5 kQpddJ cTSURq").get_text())
                    name = re.sub(r' -- .*', '', name, count=0, flags=0)
                    name = name.replace("--", ", ")
                    try: rank = str(BeautifulSoup(str(uniList[i]), 'html.parser').find("strong").get_text())
                    except Exception: rank = "?"
                    try: location = str(BeautifulSoup(str(uniList[i]), 'html.parser').find("span").get_text())
                    except Exception: location = "?"
                    # print(name, location, str(sequence), rank, sep=" | ")
                    sql = 'UPDATE unv SET (usnA&H_rank, usnA&H_sequence) = ("%s", %i) WHERE name = "%s";' % (rank, sequence, name)
                    try:
                        cur.execute(sql)
                        con.commit()
                    except Exception:
                        sql = 'INSERT INTO unv (name, location, 0, usnA&H_rank, usnA&H_sequence) VALUES ("%s", "%s", 0, "%s", %i);' % (name, location, rank, sequence)
                        try:
                            cur.execute(sql)
                            con.commit()
                        except Exception as e:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_USNews_A&H.html)\n\n')
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_USNews_A&H.html)\n\n')
            with open("QS_2022.html", 'r', encoding='utf-8') as html_file:
                html = html_file.read()
                uniList = BeautifulSoup(html, 'html.parser').find_all("td", "uni")
                uniRankList = BeautifulSoup(html, 'html.parser').find_all("td", "rank")
                sequence = 0
                for i in range(1200):
                    sequence += 1
                    rank = str(BeautifulSoup(str(uniRankList[i]), 'html.parser').find("div", "td-wrap").get_text()).strip()
                    name = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("a", "uni-link").get_text()), count=0, flags=0)
                    location = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("div", "location").get_text()).strip(), count=0, flags=0)
                    # print(name, location, str(sequence), rank, sep=" | ")
                    sql = 'UPDATE unv SET (qs2022_rank, qs2022_sequence) = ("%s", %i) WHERE name = "%s";' % (rank, sequence, name)
                    try:
                        cur.execute(sql)
                        con.commit()
                    except Exception:
                        sql = 'INSERT INTO unv (name, location, 0, qs2022_rank, qs2022_sequence) VALUES ("%s", "%s", 0, "%s", %i);' % (name, location, rank, sequence)
                        try:
                            cur.execute(sql)
                            con.commit()
                        except Exception as e:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2022.html)\n\n')
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2022.html)\n\n')
            with open("QS_2021.html", 'r', encoding='utf-8') as html_file:
                html = html_file.read()
                uniList = BeautifulSoup(html, 'html.parser').find_all("td", "uni")
                uniRankList = BeautifulSoup(html, 'html.parser').find_all("td", "rank")
                sequence = 0
                for i in range(1000):
                    sequence += 1
                    rank = str(BeautifulSoup(str(uniRankList[i]), 'html.parser').find("div", "td-wrap").get_text()).strip()
                    name = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("a", "uni-link").get_text()), count=0, flags=0)
                    location = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("div", "location").get_text()).strip(), count=0, flags=0)
                    # print(name, location, str(sequence), rank, sep=" | ")
                    sql = 'UPDATE unv SET (qs2021_rank, qs2021_sequence) = ("%s", %i) WHERE name = "%s";' % (rank, sequence, name)
                    try:
                        cur.execute(sql)
                        con.commit()
                    except Exception:
                        sql = 'INSERT INTO unv (name, location, fee, qs2021_rank, qs2021_sequence) VALUES ("%s", "%s", 0, "%s", %i);' % (name, location, rank, sequence)
                        try:
                            cur.execute(sql)
                            con.commit()
                        except Exception as e:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2021.html)\n\n')
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2021.html)\n\n')
            with open("QS_2020.html", 'r', encoding='utf-8') as html_file:
                html = html_file.read()
                uniList = BeautifulSoup(html, 'html.parser').find_all("td", "uni")
                uniRankList = BeautifulSoup(html, 'html.parser').find_all("td", "rank")
                sequence = 0
                for i in range(1000):
                    sequence += 1
                    rank = str(BeautifulSoup(str(uniRankList[i]), 'html.parser').find("div", "td-wrap").get_text()).strip()
                    name = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("a", "uni-link").get_text()), count=0, flags=0)
                    location = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("div", "location").get_text()).strip(), count=0, flags=0)
                    # print(name, location, str(sequence), rank, sep=" | ")
                    sql = 'UPDATE unv SET (qs2020_rank, qs2020_sequence) = ("%s", %i) WHERE name = "%s";' % (rank, sequence, name)
                    try:
                        cur.execute(sql)
                        con.commit()
                    except Exception:
                        sql = 'INSERT INTO unv (name, location, fee, qs2020_rank, qs2020_sequence) VALUES ("%s", "%s", 0, "%s", %i);' % (name, location, rank, sequence)
                        try:
                            cur.execute(sql)
                            con.commit()
                        except Exception as e:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2020.html)\n\n')
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2020.html)\n\n')
            with open("QS_2019.html", 'r', encoding='utf-8') as html_file:
                html = html_file.read()
                uniList = BeautifulSoup(html, 'html.parser').find_all("td", "uni")
                uniRankList = BeautifulSoup(html, 'html.parser').find_all("td", "rank")
                sequence = 0
                for i in range(1000):
                    sequence += 1
                    rank = str(BeautifulSoup(str(uniRankList[i]), 'html.parser').find("div", "td-wrap").get_text()).strip()
                    name = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("a", "uni-link").get_text()), count=0, flags=0)
                    location = re.sub(r' \(.*\)', '', str(BeautifulSoup(str(uniList[i]), 'html.parser').find("div", "location").get_text()).strip(), count=0, flags=0)
                    # print(name, location, str(sequence), rank, sep=" | ")
                    sql = 'UPDATE unv SET (qs2019_rank, qs2019_sequence) = ("%s", %i) WHERE name = "%s";' % (rank, sequence, name)
                    try:
                        cur.execute(sql)
                        con.commit()
                    except Exception:
                        sql = 'INSERT INTO unv (name, location, fee, qs2019_rank, qs2019_sequence) VALUES ("%s", "%s", 0, "%s", %i);' % (name, location, rank, sequence)
                        try:
                            cur.execute(sql)
                            con.commit()
                        except Exception as e:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2019.html)\n\n')
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + "\n" + sql + '\nInsert error (e003_QS_2019.html)\n\n')
            print("Convert done")
        except FileNotFoundError as te:
            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n\n')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n\n')
        except Exception as e:
            with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n\n')
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n\n')


