# -*- coding = utf-8 -*-
# encoding: utf-8
# @Time : 2021.12.2 14:50
# @Author : Synthesis 杜品赫
# @File : database.py
# @Software : PyCharm

import os
import sqlite3
from fchooser import *


# 初始化数据库
def db(path='db.db', table_sql="none"):
    """
    初始化数据库
    :param path: 数据库文件路径
    :param table_sql: 建表SQL文件路径
    :return: [True, con, cur] or [False, exception, "cod"]
    """
    try:
        con = sqlite3.connect(path)
        cur = con.cursor()
        try:
            if table_sql == "none":
                table_sql = fileChooser("Choose Table SQL", [('SQL file', '*.sql')])
            if readSQL(con, cur, table_sql) is True:
                return True, con, cur
        except Exception as e:
            print("Database error A01")
            print(e)
            os.remove(path)
            return False, e, "A01"
    except PermissionError as e:
        print("Database error A02")
        print(e)
        try:
            os.remove(path)
            return False, e, "A02"
        except Exception as e:
            return False, e, "A03"


def readSQL(con, cur, sql_file_path):
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql = str(file.read())
            cur.executescript(sql)
            con.commit()
        return True
    except Exception as e:
        return e
