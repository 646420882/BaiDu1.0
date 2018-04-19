import time
import pymysql
import requests
from lxml import etree

class BaiDu:
    def __init__(self,keyword):
        # Mysql配置
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.port = 3306
        self.db = 'spider'
        self.keyword = keyword

        self.url = 'http://www.baidu.com/s?wd=' + self.keyword + '&ie=UTF-8'

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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        r = requests.get(self.url, headers=headers)
        return r.text

    def parse(self,html):
        sel = etree.HTML(html)
        urls = sel.xpath('//div[@id>3000]/div[1]/h3/a/@href')  # 广告链接
        land_urls = sel.xpath('//div[@id>3000]/div[1]/h3/a/@data-landurl')  # 落地页链接
        display_urls = sel.xpath('//div[@id>3000]/div[2]/div/div[2]/div[2]/a[1]/span[1]/text()')

        a = sel.xpath('//div[@id>3000]/div[1]/h3/a')
        titles = []
        for i in a :
            title = i.xpath('string(.)')
            titles.append(title)
        ids = range(len(titles))

        for id,title,url,land_url in zip(ids,titles,urls,land_urls):
            data = {
                'id':id,
                'keyword':self.keyword,
                'title':title,
                'url':url,
                'land_url':land_url
            }
            self.save('baidu',data)


    def main(self):
        html = self.get_html()
        self.parse(html)
        print('OK')

if __name__=="__main__":
    app = BaiDu("法律咨询")
    app.main()