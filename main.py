# -*- coding = utf-8 -*-
# encoding: utf-8
# @Author : https://github.com/SynFUN / https://github.com/SynthesisDu
# @Software : PyCharm
# Python3.8

import sys
# database
import sqlite3
# other py files
from html2data import *
from data2graph import *
from pathfinder import *

# this is use for flexible input
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

# the default database initial sql
defaultSQL = """
CREATE TABLE "unv" (
"name"	TEXT NOT NULL UNIQUE,
"fee"	INTEGER,
"location"	TEXT,
PRIMARY KEY("name")
);
"""

def readSQL(sql_file_path) -> bool:
    """
    Load a [.sql] file to database
    :param sql_file_path: The [.sql] file path
    :var con: Database connection
    :var cur: Database connection cursor
    :return: True / False
    """
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


# The behavior tree
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
                    title="Save Database File",
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
                            inpC = str(input("Confirm Exit (y/n)> "))
                            if inpC in inp:
                                choose = inp[inpC]
                                if choose == 11:
                                    print("\nScript END...")
                                    sys.exit(0)
                        else: print("\nIllegal input, try again.")
                    else: print("\nIllegal input, try again.")
            elif choose == 2:
                con = sqlite3.connect(fileChooser(
                    title="Choose Database File",
                    filetypes=[('DB file', '*.db')]
                ))
                cur = con.cursor()
            elif choose == 5:
                inpC = str(input("Confirm Exit (y/n)> "))
                if inpC in inp:
                    choose = inp[inpC]
                    if choose == 11:
                        print("\nScript END...")
                        sys.exit(0)
            else: print("\nIllegal input, try again.")
            print("SQL script done.")
            print("\nConnecting Database.")
            print("+---------------------------------+")
            print("| Table structure:                |")
            for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
            print("+---------------------------------+")
            while True:
                print("a) Insert New HTML")
                print("b) Generate Graph")
                print("c) Expected Value")
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
                                        print("+---------------------------------+")
                                        print("| Table structure:                |")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                                        print("+---------------------------------+")
                                        rankTag = str(input("Name the Rank Tag Field (New or Exist)> "))
                                        sequenceTag = str(input("Name the Sequence Tag Field (New or Exist)> "))
                                        htmlPath = fileChooser(title="Choose USNews Ranking Web HTML File", filetypes=[('HTML file', '*.html')])
                                        print("Convert Start...")
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
                                        print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "s\n")
                                    if choose == 2:
                                        print("Converting USNews Rates...")
                                        print("+---------------------------------+")
                                        print("| Table structure:                |")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                                        print("+---------------------------------+")
                                        rateTag = str(input("Name the Rates Tag Field (New or Exist)> "))
                                        htmlPath = fileChooser(title="Choose USNews Rates Web HTML File", filetypes=[('HTML file', '*.html')])
                                        print("Convert Start...")
                                        time_start = time.time()
                                        error = USNRate(
                                            connect=con,
                                            cursor=cur,
                                            fileName=htmlPath,
                                            sqlKey=rateTag
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "s\n")
                                    if choose == 3:
                                        print("Converting QS Ranking...")
                                        print("+---------------------------------+")
                                        print("| Table structure:                |")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                                        print("+---------------------------------+")
                                        rankTag = str(input("Name the Rank Tag Field (New or Exist)> "))
                                        sequenceTag = str(input("Name the Sequence Tag Field (New or Exist)> "))
                                        htmlPath = fileChooser(title="Choose QS Ranking Web HTML File", filetypes=[('HTML file', '*.html')])
                                        print("Convert Start...")
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
                                        print('\nConvert done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "s\n")
                                    elif choose == 5: break
                                    else: pass
                                except FileNotFoundError as te:
                                    with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                        error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n')
                                    print("Script Error:")
                                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n')
                                except Exception as e:
                                    with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                        error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n')
                                    print("Script Error:")
                                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n')
                            else: print("\nIllegal input, try again.")
                    elif choose == 2:
                        print("\nChoose the graph type:")
                        while True:
                            print("a) 3 Axis -GIF (Disparity Graph)")
                            print("b) 3 Axis -PNG (Compare Graph)")
                            print("c) 2 Axis -PNG (Disparity Graph)")
                            print("e) Exit")
                            inpC = str(input(">>> "))
                            if inpC in inp:
                                choose = inp[inpC]
                                error = 0
                                try:
                                    if choose == 1:
                                        print("\nGenerate 3 Axis -GIF (Disparity Graph)...")
                                        print("+---------------------------------+")
                                        print("| Table structure:                |")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                                        print("+---------------------------------+")
                                        print("The field you choose must be an INTEGER or FLOAT field, not TEXT.")
                                        names = []
                                        tag1 = str(input("Choose First Axis' Field (Exist)> "))
                                        names.append(str(input("Description of the First Field> ")))
                                        tag2 = str(input("Choose Second Axis' Field (Exist)> "))
                                        names.append(str(input("Description of the Second Field> ")))
                                        tag3 = str(input("Choose Third Axis' Field (Exist)> "))
                                        names.append(str(input("Description of the Third Field> ")))
                                        title = str(input("Give a Title> "))
                                        time_start = time.time()
                                        print("Script Start...")
                                        Axis3GIF_DisparityGraph(
                                            cur=cur,
                                            x_name=tag1,
                                            y_name=tag2,
                                            z_name=tag3,
                                            names=names,
                                            titleT=title
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nGenerate done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "s\n")
                                    if choose == 2:
                                        print("\nGenerate 3 Axis -PNG (Compare Graph)...")
                                        print("+---------------------------------+")
                                        print("| Table structure:                |")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                                        print("+---------------------------------+")
                                        print("The field you choose must be an INTEGER or FLOAT field, not TEXT.")
                                        names = []
                                        tag1 = str(input("Choose First Axis' Field (Exist)> "))
                                        names.append(str(input("Description of the First Field> ")))
                                        tag2 = str(input("Choose Second Axis' Field (Exist)> "))
                                        names.append(str(input("Description of the Second Field> ")))
                                        tag3 = str(input("Choose Third Axis' Field (Exist)> "))
                                        names.append(str(input("Description of the Third Field> ")))
                                        title = str(input("Give a Title> "))
                                        time_start = time.time()
                                        print("Script Start...")
                                        Axis3PNG_CompareGraph(
                                            cur=cur,
                                            a=tag1,
                                            b=tag2,
                                            c=tag3,
                                            names=["Acceptance Rate", "Graduation Rate","International Rate"],
                                            titleT="Acceptance/Graduation/International Rate"
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nGenerate done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "s\n")
                                    if choose == 3:
                                        print("\nGenerate 2 Axis -PNG (Disparity Graph)...")
                                        print("+---------------------------------+")
                                        print("| Table structure:                |")
                                        for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                                        print("+---------------------------------+")
                                        print("The field you choose must be an INTEGER or FLOAT field, not TEXT.")
                                        tag1 = str(input("Choose First Axis' Field (Exist)> "))
                                        tag2 = str(input("Choose Second Axis' Field (Exist)> "))
                                        title = str(input("Give a Title> "))
                                        time_start = time.time()
                                        print("Script Start...")
                                        Axis2PNG_DisparityGraph(
                                            cur=cur,
                                            x_name=tag1,
                                            y_name=tag2,
                                            titleT=title
                                        )
                                        time_end = time.time()
                                        if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                                        print('\nGenerate done, ' + str(error) + ' errors happened, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "s\n")
                                    elif choose == 5: break
                                    else: pass
                                except FileNotFoundError as te:
                                    with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                        error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n')
                                    print("Script Error:")
                                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n')
                                except Exception as e:
                                    with open(r'.\error.log', 'a', encoding='utf-8') as error_file:
                                        error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n')
                                    print("Script Error:")
                                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n')
                            else: print("\nIllegal input, try again.")
                    if choose == 3:
                        try:
                            print("\nInitialize Expected Value...")
                            print("+---------------------------------+")
                            print("| Table structure:                |")
                            for i in cur.execute("PRAGMA table_info('unv')").fetchall(): print("|", i[0], i[1], " " * (20 - len(i[1]) - len(str(i[0]))), i[2], " " * (7 - len(i[2])), "|")
                            print("+---------------------------------+")
                            print("The field you choose must be an INTEGER or FLOAT field, not TEXT.")
                            print("E(X)=∑i=∑X*P(x)")
                            tag1 = str(input("[P] Choose a Rate Field (Exist)> "))
                            name1 = str(input("Description of the First Field> "))
                            tag2 = str(input("[P2] If Wants Multiple Rates (Or Left Blank)> "))
                            name2 = str(input("Description of the First Field> "))
                            tag3 = str(input("[X] Choose a Rank Field (Exist)> "))
                            name3 = str(input("Description of the First Field> "))
                            time_start = time.time()
                            print("Script Start...")
                            if tag2 != "":
                                title = "Expected Value {X=%s, P=p(%s)}" % (name3, name1)
                                expect(
                                    cur=cur,
                                    rate1=tag1,
                                    rate2=tag2,
                                    rank=tag3,
                                    titleT=title
                                )
                            else:
                                title = "Expected Value {X=%s, P=p(%s)*p(%s)}" % (name3, name1, name2)
                                expect(
                                    cur=cur,
                                    rate1=tag1,
                                    rank=tag3,
                                    titleT=title
                                )
                            time_end = time.time()
                            if (time_end - time_start) >= 60: timeCost = (time_end - time_start) / 60
                            print('\nGenerate done, ' + 'cost ' + str(round(float(time_end - time_start), 3)) + "m\n")
                        except FileNotFoundError as te:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file: error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n')
                            print("Script Error:")
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(te) + '\nOpen html_file canceled (e001)\n')
                        except Exception as e:
                            with open(r'.\error.log', 'a', encoding='utf-8') as error_file: error_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n')
                            print("Script Error:")
                            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n' + str(e) + '\nUnknown error (e002)\n')
                    elif choose == 5:
                        inpC = str(input("Confirm Exit (y/n)> "))
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
                    else: print("\nIllegal input, try again.")
                else: print("\nIllegal input, try again.")
        else: print("\nIllegal input, try again.")
