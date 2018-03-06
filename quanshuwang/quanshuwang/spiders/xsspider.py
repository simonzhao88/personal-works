import scrapy
from quanshuwang.items import QuanshuwangItem
from .paixuID import Cn2An,get_tit_num
import re


class Xsspiderspider(scrapy.Spider):
    name = "xsspider"
    allowed_domains = ["quanshuwang.com"]
    start_urls = ['http://www.quanshuwang.com/list/1_1.html']
    novel_list = []
    url = 'http://www.quanshuwang.com/list/'
    # def get_url(self,url):
    #     for i in range(1, 3):
    #         url1 = self.url + str(i) + '_'
    #         for j in range(2, 4):
    #             url2 = url1 + str(j) + '.html'
    #             print(url2)
    #             self.start_urls.append(url2)
        # return self.start_urls
    def parse(self, response):
        books = response.xpath('//*[@id="navList"]/section/ul/li/span/a[1]/@href').extract()
        # 找到每一类小说的每一本小说的下载链接
        # print(books)
        for book in books:
            # links = book.xpath('//*[@id="container"]/div[2]/section/div/div[1]/div[2]/a[1]')
            # print(links)
            # for link in links:
            #     url = link.xpath('//*[@id="container"]/div[2]/section/div/div[1]/div[2]/a[1]/@href').extract()[0]
            url = re.findall(r"http://www.quanshuwang.com/book_(\d+)",book)
            # print(url)
            url1 = "".join(url)
            # print(url1)
            url = 'http://www.quanshuwang.com/book/' + url1[:3] + '/' + url1
            # print(url)
            self.novel_list.append(url)
            self.novel_list = list(set(self.novel_list))
            for novel in self.novel_list:
                yield scrapy.Request(novel, callback=self.get_page_url)

    def get_page_url(self,response):
        '''
               找到章节链接
               '''
        page_urls = response.xpath('//*[@id="chapter"]/div[3]/div[3]/ul/div[2]/li/a/@href').extract()

        for url in page_urls:
            yield scrapy.Request(url, callback=self.get_text)

    def get_text(self,response):
        '''
                找到每一章小说的标题和正文
                并自动生成id字段，用于表的排序
                '''
        item = QuanshuwangItem()

        # 小说名
        item['bookname'] = response.xpath(
            '//*[@id="direct"]/a[3]/text()').extract()[0]

        # 章节名 ,将title单独找出来，为了提取章节中的数字
        title = response.xpath('//*[@id="directs"]/div[1]/h1/strong/text()').extract()[0]
        item['title'] = title

        #  找到用于排序的id值
        item['order_id'] = Cn2An(get_tit_num(title))

        # 正文部分需要特殊处理
        body = response.xpath('//*[@id="content"]/text()').extract()

        # 将抓到的body转换成字符串，接着去掉\t之类的排版符号，
        text = ''.join(body).strip().replace('\xa0', '').replace('\n','').replace('\r','')
        item['body'] = text
        return item

