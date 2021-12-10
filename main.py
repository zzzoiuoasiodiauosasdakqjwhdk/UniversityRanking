# -*- coding = utf-8 -*-
# encoding: utf-8
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @Software : PyCharm
# Python3.8

import sys
import sqlite3
from html2data import *
from data2graph import *
from pathfinder import *

inp = {
    # normal char
    "a": 1, "A": 1, "b": 2, "B": 2, "c": 3, "C": 3, "d": 4, "D": 4,  "g": 7, "G": 7,
    # e (exit)
    "e": 5, "E": 5, "exit": 5, "Exit": 5, "EXIT": 5, "quit": 5, "Quit": 5, "QUIT": 5,
    # h (help)
    "h": 8, "H": 8, "?": 8, "？": 8, "help": 8, "Help": 8, "HELP": 8, "": 8,
    # bool-0
    "F": 10, "f": 10, "N": 10, "n": 10, "false": 10, "False": 10, "FALSE": 10, "0": 10,
    # bool-1
    "T": 11, "t": 11, "Y": 11, "y": 11, "true": 11, "True": 11, "TRUE": 11, "1": 11
}

defaultSQL = """
CREATE TABLE "unv" (
	"name"	TEXT NOT NULL UNIQUE,
    "fee"	INTEGER,
	"location"	TEXT,
	PRIMARY KEY("name")
);
"""

def readSQL(sql_file_path):
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql = str(file.read())
            if 'CREATE TABLE "unv"' in sql:
                cur.executescript(sql)
                con.commit()
                return True
            else:
                return False
    except Exception:
        return False


if __name__ == '__main__':
    print("Initializing...")
    # 初始化Tk
    tkinter.Tk().withdraw()
    nowTime = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    print("\nNeed to connect a database file first.")
    while True:
        print("a) New DB File")
        print("b) Open DB File")
        print("e) Exit")
        inpC = str(input(">>> "))
        if inpC in inp:
            choose = inp[inpC]
            if choose == 1:
                con = sqlite3.connect(fileSaver(
                    title="Choose Database File",
                    filetypes=[('DB file', '*.db')],
                    defaultextension=".db",
                    initialfile=nowTime
                ))
                cur = con.cursor()
                print("\nGive a SQL file to initialize the table.")
                print("The SQL script should looks like this:")
                print("+----------------------------------------------------------------------------+")
                print('| CREATE TABLE "unv" ("name" TEXT NOT NULL UNIQUE, ..., PRIMARY KEY("name"); |')
                print("+----------------------------------------------------------------------------+")
                while True:
                    print("a) Choose SQL File")
                    print("b) Type In SQL")
                    print("c) Use Default Set")
                    print("e) Exit")
                    inpC = str(input(">>> "))
                    if inpC in inp:
                        choose = inp[inpC]
                        if choose == 1:
                            if readSQL(fileChooser(title="Choose Database SQL File", filetypes=[('SQL file', '*.sql')])) is True: break
                            else: print("This SQL file is not usable, try other options.")
                        elif choose == 2:
                            inpSQL = str(input("Type SQL> "))
                            if 'CREATE TABLE "unv"' in inpSQL:
                                cur.executescript(inpSQL)
                                con.commit()
                                break
                            else: print("This SQL script is not usable, try other options.")
                        elif choose == 3:
                            cur.executescript(defaultSQL)
                            con.commit()
                            break
                        elif choose == 5:
                            inpC = str(input("Confirm Exit (Y/N)> "))
                            if inpC in inp:
                                choose = inp[inpC]
                                if choose == 11:
                                    print("\nScript END...")
                                    sys.exit(0)
                        else: print("Illegal input, try again.")
                    else: print("Illegal input, try again.")
            elif choose == 2:
                con = sqlite3.connect(fileChooser(
                    title="Choose Database File",
                    filetypes=[('DB file', '*.db')]
                ))
                cur = con.cursor()
            elif choose == 5:
                inpC = str(input("Confirm Exit (Y/N)> "))
                if inpC in inp:
                    choose = inp[inpC]
                    if choose == 11:
                        print("\nScript END...")
                        sys.exit(0)
            else: print("Illegal input, try again.")
            print("SQL script done.")
            print("\nConnecting Database.")
            while True:
                print("a) Insert New HTML")
                print("e) Exit")
                inpC = str(input(">>> "))
                if inpC in inp:
                    choose = inp[inpC]
                    if choose == 1:
                        print("\nInsert new HTML, now can only accept three kind of web page:")
                        print("+-------------------------------------------------------------------------------------------------+")
                        print("| 1.USNews Ranking, eg(https://www.usnews.com/best-colleges/search?_sort=rank&_sortDirection=asc) |")
                        print("| 2.USNews Rates, eg(https://www.usnews.com/best-colleges/rankings/highest-grad-rate)             |")
                        print("| 3.QS Ranking, eg(https://www.qschina.cn/en/university-rankings/world-university-rankings/2022)  |")
                        print("+-------------------------------------------------------------------------------------------------+")
                        while True:
                            print("a) USNews Ranking")
                            print("b) USNews Rates")
                            print("c) QS Ranking")
                            print("e) Exit")
                            inpC = str(input(">>> "))
                            if inpC in inp:
                                choose = inp[inpC]
                                error = 0
                                try:
                                    if choose == 1:
                                        print("Converting USNews Ranking...")
                                        print("Table structure:")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall():
                                            print(i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2])
                                        rankTag = str(input("Name the Rank Tag Field (New or Exist)> "))
                                        sequenceTag = str(input("Name the Sequence Tag Field (New or Exist)> "))
                                        htmlPath = fileChooser(title="Choose USNews Ranking Web HTML File", filetypes=[('HTML file', '*.html')])
                                        time_start = time.time()
                                        error = USN(
                                            connect=con,
                                            cursor=cur,
                                            fileName=htmlPath,
                                            sqlKey1=rankTag,
                                            sqlKey2=sequenceTag
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "m")
                                    if choose == 2:
                                        print("Converting USNews Rates...")
                                        print("Table structure:")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall():
                                            print(i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2])
                                        rateTag = str(input("Name the Rates Tag Field (New or Exist)> "))
                                        htmlPath = fileChooser(title="Choose USNews Rates Web HTML File", filetypes=[('HTML file', '*.html')])
                                        time_start = time.time()
                                        error = USNRate(
                                            connect=con,
                                            cursor=cur,
                                            fileName=htmlPath,
                                            sqlKey=rateTag
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "m")
                                    if choose == 3:
                                        print("Converting QS Ranking...")
                                        print("Table structure:")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall():
                                            print(i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2])
                                        rankTag = str(input("Name the Rank Tag Field (New or Exist)> "))
                                        sequenceTag = str(input("Name the Sequence Tag Field (New or Exist)> "))
                                        htmlPath = fileChooser(title="Choose QS Ranking Web HTML File", filetypes=[('HTML file', '*.html')])
                                        time_start = time.time()
                                        error = QS(
                                            connect=con,
                                            cursor=cur,
                                            fileName=htmlPath,
                                            sqlKey1=rankTag,
                                            sqlKey2=sequenceTag
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "m")
                                    elif choose == 5: break
                                    else: pass
                                except FileNotFoundError as te:
                                    with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                        error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n\n')
                                    print("Script Error:")
                                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n\n')
                                except Exception as e:
                                    with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                        error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n\n')
                                    print("Script Error:")
                                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n\n')
                            else: print("Illegal input, try again. 2")
                    elif choose == 5:
                        inpC = str(input("Confirm Exit (Y/N)> "))
                        if inpC in inp:
                            choose = inp[inpC]
                            if choose == 11:
                                try:
                                    cur.close()
                                    con.close()
                                except Exception:
                                    pass
                                print("\nScript END...")
                                sys.exit(0)
                    else: print("Illegal input, try again.")
                else: print("Illegal input, try again.")
                # #############################################################################################################################################################
                # graph_3D_GIF(cur, "usn2022_sequence", "qs2022_sequence", "rate_graduation", ["USNews Rank 2022", "QS Rank 2022", "Graduation Rate"], "QS/USNews Graduation Rate")
                # graph_3D_GIF("rate_acceptance", "rate_graduation", "usn2022_sequence", ["Acceptance Rate", "Graduation Rate", "USNews Rank 2022"], "Acceptance/Graduation Rate (USNews)")
                # graph_3D_GIF("rate_acceptance", "rate_graduation", "qs2022_sequence", ["Acceptance Rate", "Graduation Rate", "QS Rank 2022"], "Acceptance/Graduation Rate (QS)")
                # graph_3D_GIF("qs2022_sequence", "qs2021_sequence", "qs2020_sequence", ["QS Rank 2022", "QS Rank 2021", "QS Rank 2020"], "QS 2022-2020")
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
        else: print("Illegal input, try again.")

