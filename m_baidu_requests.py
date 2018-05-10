import time
import pymysql
import requests
import re
import random
from lxml import etree

class BaiDu:
    def __init__(self):
        # Mysql配置
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.port = 3306
        self.db = 'spider'
        self.table = 'result'

        self.filename = 'M关键词.txt'
        self.sleep = 1
        self.keywords = []
        self.keyword = ''

    def get_keywords(self):
        with open(self.filename, 'r',encoding="utf-8") as f:
            self.keywords = f.read().splitlines()

    def get_html(self):
        # UA = random.choice(UA_list)
        # headers = {'User-Agent': UA}
        #移动
        headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Mobile Safari/537.36'}
        #PC
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        r = requests.get(self.url, headers=headers)
        return r.text

    def parse(self,html):
        sel = etree.HTML(html)
        search_day = time.strftime("%Y-%m-%d", time.localtime())  # 日期
        search_time = time.strftime("%H:%M:%S", time.localtime())  # 时间
        sel = sel.xpath('//div[@class="ec_ad_results" and @posid="1" and @prank="1"]')[0]
        sels = sel.xpath('./div[@data-rank]')
        for a in sels:
            try:
                display_url = a.xpath(
                    './div/div[@class="c-showurl c-line-clamp1"]/div[@class="ec_urlline"]/a/span[@class="c-showurl"]/text()')[0]
                title = a.xpath('.//h3')[0].xpath('string(.)')
                url = a.xpath('.//a[@class="c-blocka ec_title "]/@href')[0]
                print(title)
                print(display_url)
                print(url)

            except:
                pass
        rank = 1
        for id in ids:
            try:
                sel1 = sel.xpath('//div[@id=%s]' % id)[0]
                title = sel1.xpath('./div[1]/h3/a')[0].xpath('string(.)')  # 标题
                url = sel1.xpath('./div[1]/h3/a/@href')[0]  # 广告链接
                land_url = sel1.xpath('./div[1]/h3/a/@data-landurl')[0]  # 落地页链接
                display_url = re.search('://(.*?)/', land_url, re.S).group(1)  # 显示连接
                data = {
                    'search_engine': '百度',
                    'search_type': 'PC',
                    'search_date': search_day,
                    'search_time': search_time,
                    'search_ranking': rank,
                    'keyword': self.keyword,
                    'title': title,
                    'url': url,
                    'disp_id': id,
                    'land_url': land_url,
                    'display_url': display_url
                }
                rank +=1
                print(data)
                self.save(data)
            except:
                #print('%s not found' % id)
                pass
        #driver.close()

    def save(self,data):
        db = pymysql.connect(host=self.host, user=self.user, password=self.password, port=self.port, db=self.db,
                             charset='utf8')
        cursor = db.cursor()
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=self.table, keys=keys, values=values)
        try:
            if cursor.execute(sql, tuple(data.values())):
                db.commit()
        except:
            print('Failed')
            db.rollback()
        finally:
            db.close()

    def main(self):
        self.get_keywords()
        for keyword in self.keywords:
            self.keyword = keyword
            self.url = 'https://www.baidu.com/s?wd=' + self.keyword + '&ie=UTF-8'
            html = self.get_html()
            self.parse(html)
            #time.sleep(self.sleep)
            #time.sleep(random.random())



if __name__=="__main__":
    app = BaiDu()
    app.main()
    print('查询完成')