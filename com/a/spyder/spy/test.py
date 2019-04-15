#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : test.py
# @Author  : A
# @Time    : 2019/4/13 17:25
# @Contact : qq1694522669@gmail.com

from com.a.spyder.spy.spiderRun import SpiderRun

if __name__ == '__main__':

    jdthread = SpiderRun(1, "python")
    suningthread = SpiderRun(2, "python")
    jdthread.start()
    suningthread.start()
    while True:
        string = input()
        if string == "#":
            print("————————————————————————————————————————")
            jdthread.stop()
            suningthread.stop()
            break
