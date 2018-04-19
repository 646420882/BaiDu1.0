import time
import requests
from lxml import etree

class BaiDu:
    def __init__(self,keyword):
        self.url = 'http://www.baidu.com/s?wd=' + keyword + '&ie=UTF-8'

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

        for title,url,land_url,display_url in zip(titles,urls,land_urls,display_urls):
            print('标题：%s\n链接：%s\n落地页：%s\n显示URL：%s\n'%(title,url,land_url,display_url))


    def main(self):
        html = self.get_html()
        self.parse(html)
        print('OK')

if __name__=="__main__":
    app = BaiDu("广州律师事务所")
    app.main()