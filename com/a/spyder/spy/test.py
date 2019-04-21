#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : test.py
# @Author  : A
# @Time    : 2019/4/13 17:25
# @Contact : qq1694522669@gmail.com

from com.a.spyder.spy.spiderRun import SpiderRun

if __name__ == '__main__':

    jdthread = SpiderRun(1, "娃哈哈")
    # 参数1-京东、2-苏宁易购，字符串代表关键词
    suningthread = SpiderRun(2, "娃哈哈")
    jdthread.start()
    suningthread.start()
    while True:
        string = input()
        if string == "#":
            print("————————————————————————————————————————")
            jdthread.stop()
            # 在下一个搜索的时候调用停止
            suningthread.stop()
            break
