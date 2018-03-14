from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import error
from urllib.request import Request
import random
import re
import sqlite3
import time
import numpy as np


headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
def get_house_info(urls,html):
    for url in urls:
        time.sleep(np.random.rand() * 5)
        try:
            res = Request(url,headers=headers[random.randint(0,2)])
            response= urlopen(res)
            soup = BeautifulSoup(response,'lxml')
        except (error.HTTPError, error.URLError) as e:
            print(e)
            continue
        #title
        title_list = soup.select('body > div.main-wrap > div.house-title > h1')
        for i in title_list:
            title = "".join(i.getText())
            # print(title)
        #url
        house_list = html.select('body > div.mainbox > div.main > div.content > div.listBox > ul > li > div.des > h2 > a')
        for i in house_list:
            house_url = "".join(i.get('href'))
            # print(house_url)
        #价格list
        price_list = soup.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b')
        for i in price_list:
            price = "".join(re.findall(r'b class="f36">(\d+)',str(i)))
            # print(price)
        #图片urls
        img_urls = soup.findAll('ul',{'class':'house-pic-list'})
        for i in img_urls:
            img_url = ",".join(re.findall(r'img lazy_src="(.*?)"',str(i)))
            # print(img_url)
        #地址list
        add_list = soup.select('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li > span.dz')
        for i in add_list:
            add = "".join(i.getText().strip())
            # print(add)
        # return title,price,img_url,add
        # 存入数据库
        conn = sqlite3.connect('houseinfo.db')
        cur = conn.cursor()
        try:
            sql1 = 'create table if not exists house_info(title CHAR(30),houseurl CHAR(50),price CHAR(5),imgurl text,address CHAR(30))'
            sql2 = 'insert into  house_info values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' %(title,house_url,price,img_url,add)
            cur.execute(sql1)
            cur.execute(sql2)
            conn.commit()
        finally:
            conn.close()