#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : spiderRun.py
# @Author  : A
# @Time    : 2019/4/14 14:40
# @Contact : qq1694522669@gmail.com
import threading

from com.a.spyder.spy.jd import JdSpider
from com.a.spyder.spy.suning import SuningSpider


class SpiderRun(threading.Thread):
    def __init__(self, type, string):
        super(SpiderRun, self).__init__()
        self.jdspider = JdSpider()
        self.suningspider = SuningSpider()
        self.string = string
        self.type = type

    def stop(self):
        self.suningspider.change_State()
        self.jdspider.change_State()
        pass

    def run(self):
        if self.type == 1:
            self.jdspider.crawl(self.string)
        elif self.type == 2:
            self.suningspider.crawl(self.string)
