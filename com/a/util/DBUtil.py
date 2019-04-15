#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : DBUtil.py
# @Author  : A
# @Time    : 2019/4/1 13:42
# @Contact : qq1694522669@gmail.com

import pymysql


class DBUtil:
    def __init__(self):
        self.__db = pymysql.connect("95.163.197.217", "root", "201269", "mysql", use_unicode=True, charset='utf8')
        self.__cursor = self.__db.cursor()

    def getConnect(self):
        return self.__db

    def getCursor(self):
        return self.__cursor

    def closeCursor(self):
        self.__cursor.close()

    def closeConnect(self):
        self.__db.close()
