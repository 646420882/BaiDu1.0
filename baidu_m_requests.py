#!usr/bin/python
# -*- coding:utf-8 -*-
import time
import pymysql
import requests
from lxml import etree
from multiprocessing import Pool

keywords_filename = '百度_M_关键词.txt'

class Spider:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.port = 3306
        self.db_name = 'spider'
        self.table_name = 'result'
        self.index = 'https://www.baidu.com/s?wd='
        self.search_engine = '百度'
        self.search_type = 'M'
        self.keyword = None

    def get_html(self):
        if self.search_type == 'PC' or self.search_type == 'pc':
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        else:
            headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'}
        r = requests.get(self.url, headers=headers)
        return r.text

    def parse(self,html):
        sel = etree.HTML(html)
        search_day = time.strftime("%Y-%m-%d", time.localtime())  # 日期
        search_time = time.strftime("%H:%M:%S", time.localtime())  # 时间
        sel = sel.xpath('//div[@class="ec_ad_results"]/div[@data-rank]')
        rank = 1
        for sel1 in sel:
            try:
                display_url = sel1.xpath(
                    './div/div[@class="c-showurl c-line-clamp1"]/div[@class="ec_urlline"]/a/span[@class="c-showurl"]/text()')[
                    0]
                title = sel1.xpath('.//h3')[0].xpath('string(.)')
                data = {
                    'search_engine': self.search_engine,
                    'search_type': self.search_type,
                    'search_date': search_day,
                    'search_time': search_time,
                    'search_ranking': rank,
                    'keyword': self.keyword,
                    'title': title,
                    'display_url': display_url
                }
                rank += 1
                print(data)
                self.save_mysql(data)
            except:
                pass

    def save_mysql(self,data):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db_name,
                             charset='utf8')
        cursor = db.cursor()
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=self.table_name, keys=keys, values=values)
        try:
            if cursor.execute(sql, tuple(data.values())):
                db.commit()
        except:
            print('Save to mysql failed!')
            db.rollback()
        finally:
            db.close()

    def main(self,keyword):
        self.keyword = keyword
        self.url = self.index + self.keyword
        html = self.get_html()
        self.parse(html)

def get_keywords(keywords_filename):
    with open(keywords_filename, 'r', encoding="utf-8") as f:
        keywords = f.read().splitlines()
        for keyword in keywords:
            yield keyword

if __name__=="__main__":
    start_time = time.time()
    app = Spider()
    pool = Pool(10)  # processes = 10  开启进程数，默认为系统核心数
    pool.map(app.main, get_keywords(keywords_filename))
    pool.close()
    pool.join()
    times = time.time()- start_time
    print('耗时%s秒'%round(times,1))