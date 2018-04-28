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
        self.table = 'baidu'

        self.filename = '关键词.txt'
        self.sleep = 10
        self.keywords = []
        self.keyword = ''

    def get_keywords(self):
        with open(self.filename, 'r',encoding="utf-8") as f:
            self.keywords = f.read().splitlines()

    def save(self,table,data):
        db = pymysql.connect(host=self.host,user=self.user,password=self.password,port=self.port,db=self.db,charset='utf8')
        cursor = db.cursor()
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        try:
            if cursor.execute(sql, tuple(data.values())):
                print('Successful')
                db.commit()
        except:
            print('Failed')
            db.rollback()
        db.close()

    def get_html(self):
        UA_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        #UA = random.choice(UA_list)
        #headers = {'User-Agent': UA}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        print(headers)
        r = requests.get(self.url, headers=headers)
        return r.text

    def parse(self,html):
        a = 1
        sel = etree.HTML(html)

        pattern = re.compile('.ec-showurl-lh20 .(.*?){line-height:20px}',
                             re.S)
        try:
            class_name = re.findall(pattern, html)[0]  # 显示URL的classname
            pattern = '//div[@id>3000]//span[@class="%s"]/text()' % class_name
        except:
            a = 0
            print(html)
            print('当前显示无广告？')
        if a :
            urls = sel.xpath('//div[@id>3000]/div[1]/h3/a/@href')  # 广告链接
            land_urls = sel.xpath('//div[@id>3000]/div[1]/h3/a/@data-landurl')  # 落地页链接
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            titles = []
            a = sel.xpath('//div[@id>3000]/div[1]/h3/a')
            for i in a:
                title = i.xpath('string(.)')
                titles.append(title)
            rankings = range(1, len(titles) + 1)

            display_urls = sel.xpath(pattern)
            if len(urls) == len(display_urls):
                for ranking, title, url, land_url, display_url in zip(rankings, titles, urls, land_urls, display_urls):
                    data = {
                        'engine': 'baidu',
                        'type': 'PC',
                        'time': times,
                        'ranking': ranking,
                        'keyword': self.keyword,
                        'title': title,
                        'url': url,
                        'land_url': land_url,
                        'display_url': display_url
                    }
                    print(data)
                    #self.save(self.table, data)
            else:
                print('数据未对齐')
        else:
            print('无结果：%s'%self.keyword)



    def main(self):
        self.get_keywords()
        for keyword in self.keywords:
            print('当前关键词：%s'%keyword)
            self.keyword = keyword
            self.url = 'http://www.baidu.com/s?wd=' + self.keyword + '&ie=UTF-8'

            self.parse(self.get_html())
            time.sleep(self.sleep)



if __name__=="__main__":
    app = BaiDu()
    app.main()