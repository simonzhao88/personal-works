import threading
from time import sleep
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
import os

# ajax请求的目标基本网址
base_url = 'http://www.mmjpg.com/data.php?'
# 图片的基本网址
pic_base_url = 'http://img.mmjpg.com/2018/'

headers = {
    'Host': 'www.mmjpg.com',
    'Referer': 'http://www.mmjpg.com/mm/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def pic_num():
    """
    获取首页每个图片集的图片编号
    :return:带有图片集编号的list
    """
    pic_no = []
    pages = int(input('请输入要爬取的页数：'))
    for page in range(1, pages+1):
        if page == 1:
            url = 'http://www.mmjpg.com'
        else:
            url = 'http://www.mmjpg.com/home/' + str(page)
        res = requests.get(url, headers=headers).text.encode('ISO 8859-1').decode('utf-8')
        soup = BeautifulSoup(res, 'lxml')
        urls = soup.select('body > div.main > div.pic > ul > li > span.title > a')
        for url in urls:
            data = {}
            title = url.string
            pic_id = url.get('href').split('/')[-1]
            data['title'] = title
            data['pic_num'] = pic_id
            pic_no.append(data)
    return pic_no


def pic_data(pic_no):
    """
    获取ajax请求后返回的图片地址数据
    :param pic_no: 带有图片集编号的list
    :return: 带有图片地址数据的list
    """
    url_data_list = []
    for url in pic_no:
        data = {}
        pic_num1 = url['pic_num']
        headers1 = {
            'Host': 'www.mmjpg.com',
            'Referer': 'http://www.mmjpg.com/mm/' + str(pic_num1),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        data['title'] = url['title']
        data['pic_num'] = pic_num1
        params = {
            'id': pic_num1,
            'page': '8999'
        }
        url = base_url + urlencode(params)
        try:
            response = requests.get(url, headers=headers1)
            if response.status_code == 200:
                res = response.text
                data['pid'] = list(i for i in res.split(','))
                url_data_list.append(data)
        except requests.ConnectionError as e:
            print('Error', e.args)
    return url_data_list


def pic_url(url_lists):
    """
    将图片的基本地址和图片数据拼接成完整的图片地址
    :param url_lists: 带有图片地址数据的list
    :return: 返回带有图片完整地址的list
    """
    pic_urls_list = []
    for urls in url_lists:
        pic_url_dict = {}
        pic_urls = []
        pic_url_dict['title'] = urls['title']
        pic_num2 = urls['pic_num']
        url_list1 = urls['pid']
        pic_url_dict['pic_num'] = pic_num2
        if url_list1:
            for i in range(1, len(url_list1) + 1):
                pic_url1 = pic_base_url + str(pic_num2) + '/' + str(i) + 'i' + url_list1[i - 1] + '.jpg'
                pic_urls.append(pic_url1)
            pic_url_dict['picurl'] = pic_urls
            pic_urls_list.append(pic_url_dict)
    # print(pic_urls_list)
    return pic_urls_list


def download(filename, pic_num2, url):
    """
    根据图片地址下载图片到本地
    :param filename: 文件名
    :param pic_num2: 图片编号
    :param url: 图片地址
    :return:
    """
    header = {
        'Referer': 'http://www.mmjpg.com/mm/' + str(pic_num2),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    res = requests.get(url, headers=header).content
    # print(res)
    path = 'mmpic/' + filename + '/' + url.split('/')[-1]
    # print(path)
    with open(path, 'wb') as f:
        f.write(res)


def start(pic_url_list):
    """
    多线程下载图片，每一次下载就分配一个线程取执行download
    :param pic_url_list: 带有图片完整地址的list
    :return:
    """
    for pic_urls in pic_url_list:
        pic_num2 = pic_urls['pic_num']
        filename = pic_urls['title']
        pic_url2 = pic_urls['picurl']
        if not os.path.exists('mmpic/' + filename):
            os.mkdir('mmpic/' + filename)
        for url in pic_url2:
            thread = threading.Thread(target=download, args=(filename, pic_num2, url))
            thread.start()
        sleep(0.5)
        print(filename + '下载完成~~')
    print('全部图片下载完成~~~')


if __name__ == '__main__':
    url_list = pic_data(pic_num())
    pic_url(url_list)
    start(pic_url(url_list))
