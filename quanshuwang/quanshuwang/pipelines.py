# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QuanshuwangPipeline(object):
    def process_item(self,item,spider):
        '''
               将爬到的小数写入数据库
               '''

        # 首先从items里取出数据
        name = item['bookname']
        order_id = item['order_id']
        body = item['body']
        title = item['title']

        # 与本地数据库建立联系
        # 和本地的scrapyDB数据库建立连接
        connection = pymysql.connect(
            host='192.168.100.103',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='root',  # 自己的密码
            db='database_test',  # 数据库的名字
            charset='utf8mb4', # 默认的编码方式：
            port=3306,
            cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # 数据库表的sql
                sql1 = 'Create Table If Not Exists %s(id int,zjm varchar(100),body text)' % name
                # 单章小说的写入
                sql = 'Insert into %s values (%d ,\'%s\',\'%s\')' % (name, order_id, title, body)
                cursor.execute(sql1)
                cursor.execute(sql)

            # 提交本次插入的记录
            connection.commit()
        finally:
            # 关闭连接
            connection.close()
        return item
