#!/usr/bin/env python
# encoding: utf-8
'''
@author: tiankunpeng

@file: selenium_baidu.py

@time: 2018/4/27 14:29
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.blocking import BlockingScheduler
import time





def init_search(key):
    driver = webdriver.Chrome(executable_path="./chromedriver.exe")  # Chrome
    #driver = webdriver.Firefox(executable_path='./geckodriver.exe') # firfox webdriver  会弹出浏览器
    #driver = webdriver.PhantomJS(executable_path='./phantomjs.exe') # PhantomJS webdriver  这个不会弹出浏览器 如果要用 请自行百度下载
    #driver.maximize_window()
    driver.get('https://www.baidu.com')
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "kw"))
        )
        element.send_keys(key)
        button = driver.find_element_by_id('su')
        button.click()
        return driver
    except:
        pass


def get_infos(driver):
    get_info(driver)
    page_index = 1
    page_num = 1
    try:
        while page_index<page_num:
            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'n'))
                )
            except:
                driver.refresh()
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'n'))
                )
            next_page_button.click()

            get_info(driver)
            page_index = page_index + 1

    except:
        driver.quit()
    finally:
        driver.quit()




def get_info(driver):
    ids = [3001, 3002, 3003, 3004, 3005]
    for url_id in ids:
        try:
            target_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, str(url_id)))
            )
            if target_element:
                info_dic = {}
                info_dic['context'] = target_element.text
                info_dic['popularize_url'] = target_element.find_element_by_xpath('./div/h3/a').get_attribute('href')
                info_dic['target_url'] = target_element.find_element_by_xpath('./div/h3/a').get_attribute(
                    'data-landurl')
                info_dic['title'] = target_element.find_element_by_xpath('./div/h3/a').text
                print(info_dic)
                """
                补充下扔到你数据库就好
                """
        except:
            print('not get info from %s' % str(url_id))

def get_words():
    """
    搜索关键字部分
    :return:
    """
    with open('关键词.txt', 'r', encoding="utf-8") as f:
        key_words = f.read().splitlines()
    #key_words = ['律师事务所', '离婚诉讼律师']
    for i in key_words:
        print(i)
        yield i

def do_work():
    for tmp_word in get_words():
        driver = init_search(key=tmp_word)
        get_infos(driver)


if __name__ =="__main__":
    #sched = BlockingScheduler()
    #sched.add_job(do_work, 'interval', hour=1)  # 每三分钟执行一次 如果设置没小时执行一次 hour=1 即可sched.add_job(do_work, 'interval', hour=1)
    #sched.start()
    do_work()
    pass

pass


