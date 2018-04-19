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
        self.table = 'baidu'

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
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        titles = []
        a = sel.xpath('//div[@id>3000]/div[1]/h3/a')
        for i in a :
            title = i.xpath('string(.)')
            titles.append(title)
        rankings = range(1,len(titles)+1)
        display_urls = []
        for land_url in land_urls:
            if 'https' in land_url:
                display_url = land_url.split('https://')[1].split('/')[0]
            else:
                display_url = land_url.split('http://')[1].split('/')[0]
            display_urls.append(display_url)
        if len(urls)==len(display_urls):
            for ranking, title, url, land_url, display_url in zip(rankings, titles, urls, land_urls, display_urls):
                data = {
                    'time': times,
                    'ranking': ranking,
                    'keyword': self.keyword,
                    'title': title,
                    'url': url,
                    'land_url': land_url,
                    'display_url': display_url
                }
                self.save(self.table, data)
        else:
            print('titles:',titles)
            print('urls:', urls)
            print('land_urls:', land_urls)
            print('display_urls:', display_urls)
            print('rankings:', rankings)
            print('数据未对齐')

    def main(self):
        html = self.get_html()
        self.parse(html)

if __name__=="__main__":
    app = BaiDu("律师事务所")
    app.main()