#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : __init__.py.py
# @Author  : A
# @Time    : 2019/4/1 13:42
# @Contact : qq1694522669@gmail.com
from com.a.util import DBUtil

if __name__ == "__main__":
    db = DBUtil()
    cursor = db.getCursor()
    INSERT_ITEMS = "INSERT INTO items (link, price, itemname) VALUES ({0}, {1}, {2})".format("111", "111.0", "111")
    cursor.execute(INSERT_ITEMS)
    db.closeConnect()
    print(db)
    print(cursor)
