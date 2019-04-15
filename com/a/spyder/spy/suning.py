from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

# from sn_config import *
from selenium.webdriver.common.keys import Keys
from pyquery import PyQuery as pq

from com.a.persisitence.ItemsDAO import ItemsDAO


class SuningSpider:

    # browser = webdriver.PhantomJS(service_args=SERVICE_ASK)  # 无可视化的浏览器,需安装插件
    def __init__(self):
        self.isStop = False
        self.itemsDAO = ItemsDAO()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)

    # browser = webdriver.Chrome() # 可视化浏览器

    def change_State(self):
        if self.isStop:
            self.isStop = False
        else:
            self.isStop = True

    def search(self, keyword):
        # 请求苏宁易购首页
        self.browser.get('https://www.suning.com/')
        # 找到输入的搜索框
        _input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#searchKeywords'))
        )
        # 找到搜索按钮
        submit = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#searchSubmit")))
        _input.send_keys(keyword)
        submit.click()
        # 找到总页数
        target = self.browser.find_element_by_css_selector('#bottom_pager > div > span.page-more')
        self.browser.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(3)
        total = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#bottom_pager > div > span.page-more')))
        # 对找到的总页数进行正则处理，并返回int类型的页数
        _total = total.text
        # print(_total)
        pattern = re.compile('\S\S(\d+).*?')
        result = re.search(pattern, _total)
        self.parse_html()
        return int(result.group(0)[1:])

    def next_page(self, page):
        print('正在翻页', page)
        try:
            # 找到页数的输入框
            time.sleep(1)
            inputs = WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#bottomPage')))
            time.sleep(1)
            inputs.clear()
            # 找到确定的按钮
            submit = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#bottom_pager > div > a.page-more.ensure")))
            inputs.send_keys(page)
            submit.send_keys(Keys.ENTER)
            target = self.browser.find_element_by_css_selector('#bottom_pager > div > span.page-more')
            self.browser.execute_script("arguments[0].scrollIntoView();", target)  # 将页面下拉至底部休息3秒等待数据加载
            time.sleep(3)
            # 进行判定：高亮下的页数是否和输入框的一致
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#bottom_pager > div > a.cur')), str(page))
            self.parse_html()
        except Exception as e:
            print(e.args)
            self.next_page(page)

    def parse_html(self):
        try:
            # 选择整个展示框
            WebDriverWait(self.browser, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#product-list .item-wrap')))
            # product-list
            html = self.browser.page_source
            doc = pq(html)
            # 拿到所有的item，进行迭代，拿到所有商品的数据
            items = doc('#product-list .item-wrap').items()
            string = ""
            count = 0
            for item in items:
                count += 1
                products = {
                    'price': item.find('.def-price').text().replace('\n', ' '),
                    'description': item.find('.title-selling-point').text().strip().replace('\n', ' '),
                    'url': item.find('.title-selling-point'),
                    'img': item.find('.sellPoint')
                }
                if products['price'] == "":
                    continue
                # print(products['price'])
                temp = products['price'].split("¥")
                # print(temp)
                products['price'] = temp[1][:-1]
                for a in item.find('.title-selling-point').find('a'):
                    products['url'] = a.get('href')
                for a in item.find('.img-block').find('a'):
                    products['img'] = a.find('img').get('src')
                string += products['url'] + "$$" + products['price'] + "$$" + products['description'] + "$$" + products[
                    'img'] + "$$2" + "\n"
                print(count)
                if count == 60:
                    count = 0
                    self.itemsDAO.insertData(string)

                print(string)
        except TimeoutError:
            self.parse_html()

    def crawl(self, keyword):
        try:
            total = self.search(keyword)  # 得到的总页数
            for i in range(2, total + 1):
                self.next_page(i)
                time.sleep(2)
                if self.isStop:
                    break
        except Exception as e:
            print(e.args)
        finally:
            self.browser.close()
