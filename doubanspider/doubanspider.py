# -*- coding: UTF-8 -*-
import sys
import time
from urllib.request import urlopen
from urllib.parse import quote
from urllib import error
import urllib
from urllib.request import Request
import numpy as np
from bs4 import BeautifulSoup
from imp import reload
import sqlite3


class doubanspider():
    reload(sys)
    # 构建请求头
    headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
    page_num = 0
    book_list = []
    try_times = 0
    def book_spider(self,book_tag_lists):
        list_soups = []
        for book_tag in book_tag_lists:
            for page_num in range(5):
                url = 'http://www.douban.com/tag/' + quote(book_tag) + '/book?start=' + str(page_num * 15)
                # 随机选择时间睡眠
                time.sleep(np.random.rand() * 5)
                try:
                    req = Request(url, headers=self.headers[page_num % len(self.headers)])
                    source_code = urlopen(req).read()
                    plain_text = str(source_code,'utf-8')
                except (error.HTTPError, error.URLError) as e:
                    print(e)
                    continue
                soup = BeautifulSoup(plain_text, 'lxml')
                list_soup = soup.find('div', {'class': 'mod book-list'})
                self.try_times += 1;
                if list_soup == None and self.try_times < 200:
                    continue
                elif list_soup == None or len(list_soup) <= 1:
                    break  # 超过200次或list_soup无数据尝试跳出循环
                list_soups.append(list_soup)
        return list_soups
    #获取书籍信息
    def get_book_info(self,list_soups):
        for list_soup in list_soups:
            for book_info in list_soup.select('dd'):
                # print(book_info)
                #书名
                title = book_info.find('a', {'class': 'title'}).string.strip()
                print(title)
                desc = book_info.find('div', {'class': 'desc'}).string.strip()
                desc_list = desc.split('/')#['[哥伦比亚] 加西亚·马尔克斯 ', ' 范晔 ', ' 南海出版公司 ', ' 2011-6 ', ' 39.50元']
                book_url = book_info.find('a', {'class': 'title'}).get('href')
                # 获取评分
                try:
                    rating = book_info.find('span', {'class': 'rating_nums'}).string.strip()
                except:
                    rating = 0.0
                # 获取出版信息
                try:
                    pub_info = '/'.join(desc_list[-3:-2])
                    # print(pub_info)
                except:
                    pub_info = '出版信息： 暂无'
                #获取译者
                try:
                    translators = '/'.join(desc_list[-4:-3])
                    # print(translators)
                except:
                    translators = '译者： 暂无'
                try:
                    publication_year =  '/'.join(desc_list[-2:-1])
                    # print(publication_year)
                except:
                    publication_year = '出版年份： 暂无'
                #图书价格
                try:
                    book_price = '/'.join(desc_list[-1:])
                    # print(book_price)
                except:
                    book_price = '图书价格： 暂无'
                try:
                    req = Request(book_url, headers=self.headers[np.random.randint(0, len(self.headers))])
                    source_code = urlopen(req).read()
                    plain_text = str(source_code, 'utf-8')
                except (error.HTTPError, error.URLError) as e:
                    print(e)
                soup = BeautifulSoup(plain_text, 'lxml')
                #获取作者
                try:
                    author_info = '/'.join(desc_list[:1])
                        # print(author_info)
                except:
                    author_info = translators
                #评论人数
                try:
                    people_num = int(soup.find('div', {'class': 'rating_sum'}).findAll('span')[1].string.strip('人评价'))
                    # print(people_num)
                except:
                    people_num = 0

                # 将书籍信息写入数据库
                con = sqlite3.connect('shuji.db')
                cursor = con.cursor()
                try:
                    sql1 = 'create table  If Not Exists  book(fid INTEGER PRIMARY KEY autoincrement,title char(20),author_info char(30),pub_info char(50),people_num int,rating INT,translators CHAR(15), publication_year CHAR(10),book_price CHAR(15))'
                    sql2 = 'insert into book (title, author_info, pub_info, people_num, rating, translators, publication_year,book_price) VALUES (\'%s\',\'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\',\'%s\')' % (
                    title, author_info, pub_info, people_num, rating, translators, publication_year, book_price)
                    cursor.execute(sql1)
                    cursor.execute(sql2)
                    con.commit()
                finally:
                    cursor.close()
                self.book_list.append([title, rating, people_num, author_info, pub_info, translators, publication_year, book_price])
                '''需要的数据：
                        书名、作者、评分、译者、出版社、出版年、页数、定价、ISBN、评论人数
                        '''
            try_times = 0  # 将尝试次数归零
            self.page_num += 1
            print('从%d页下载信息!' % self.page_num)


