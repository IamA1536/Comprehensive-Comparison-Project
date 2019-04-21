#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ItemsDAO.py
# @Author  : A
# @Time    : 2019/4/1 14:19
# @Contact : qq1694522669@gmail.com
from com.a.util import DBUtils


class ItemsDAO:

    def __init__(self):
        self.__INSERT_ITEMS = "INSERT INTO items (link, price, itemname, img, itemfrom) VALUES (%s, %s, %s,%s,%s)"
        self.__TRUNCATE_TABLE = "TRUNCATE TABLE items"
        pass

    def insertData(self, str):
        temp = []
        count = 0
        for line in str.split("N\n"):
            temps = line.split("$$")
            count += 1
            temp.append(temps)
        temp.remove([''])
        print(temp)
        # sql_str = self.__INSERT_ITEMS.format(temp[0], temp[1], temp[2], temp[3])
        # print(sql_str)
        db = DBUtils()
        connect = db.getConnect()
        cursor = db.getCursor()
        cursor.executemany(self.__INSERT_ITEMS, temp)
        # cursor.execute(sql_str)
        connect.commit()
        db.closeCursor()
        db.closeConnect()
        pass

    def clearData(self):
        db = DBUtils()
        cursor = db.getCursor()
        cursor.execute(self.__TRUNCATE_TABLE)
        db.closeConnect()

