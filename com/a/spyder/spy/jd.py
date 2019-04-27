#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : jd.py
# @Author  : A
# @Time    : 2019/4/9 15:13
# @Contact : qq1694522669@gmail.com

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
import time

from com.a.persisitence.ItemsDAO import ItemsDAO


class JdSpider:
    def __init__(self):
        self.isStop = False

    # def open_file(self):
    #     self.fd = open('Jd.txt', 'w', encoding='utf-8')

    def change_State(self):
        if self.isStop:
            self.isStop = False
        else:
            self.isStop = True

    def open_browser(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome("../driver/chromedriver.exe", chrome_options=chrome_options)
        self.browser.implicitly_wait(10)
        self.wait = WebDriverWait(self.browser, 10)

    def init_variable(self):
        self.data = zip()
        self.isLast = False

    def parse_page(self):

        try:
            skus = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//li[@class="gl-item"]')))
            skus = [item.get_attribute('data-sku') for item in skus]
            links = ['https://item.jd.com/{sku}.html'.format(sku=item) for item in skus]
            prices = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gl-i-wrap"]/div[2]/strong/i')))
            prices = [item.text for item in prices]
            names = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gl-i-wrap"]/div[3]/a/em')))
            names = [item.text for item in names]
            img = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gl-i-wrap"]/div[1]/a/img')))
            imgs = []
            for item in img:
                if item.get_attribute('src') is None:
                    imgs.append(item.get_attribute('data-lazy-img'))
                else:
                    imgs.append(item.get_attribute('src'))
            self.data = zip(links, prices, names, imgs)
        except selenium.common.exceptions.TimeoutException:
            print('parse_page: TimeoutException')
            self.parse_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('parse_page: StaleElementReferenceException')
            self.browser.refresh()

    def turn_page(self):
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="pn-next"]'))).click()
            time.sleep(1)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
        except selenium.common.exceptions.NoSuchElementException:
            self.isLast = True
        except selenium.common.exceptions.TimeoutException:
            print('turn_page: TimeoutException')
            self.turn_page()
        except selenium.common.exceptions.StaleElementReferenceException:
            print('turn_page: StaleElementReferenceException')
            self.browser.refresh()

    def write_to_file(self, itemsDAO):
        string = ""
        count = 0
        for item in self.data:
            count += 1
            string += str(item[0]) + "$$" + str(item[1]) + "$$" + str(item[2]) + "$$" + str(item[3]) + "$$1" + "N\n"
            if count == 30:
                count = 0
                itemsDAO.insertData(string)
            # print(string + "\n")
            # self.fd.write(string + "\n")

    def close_file(self):
        self.fd.close()

    def close_browser(self):
        self.browser.quit()

    def crawl(self, keyword):
        # self.open_file()
        self.open_browser()
        self.init_variable()
        # print('开始爬取')

        self.browser.get('https://search.jd.com/Search?keyword=' + keyword + '&enc=utf-8')
        time.sleep(1)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        count = 0
        itemsDAO = ItemsDAO()

        while not self.isLast:
            count += 1
            print('正在爬取第 ' + str(count) + ' 页......')
            self.parse_page()
            self.write_to_file(itemsDAO)
            self.turn_page()
            if self.isStop:
                self.isStop = False
                # itemsDAO.clearData()
                break
        # self.close_file()
        self.close_browser()
        # print('结束爬取')
