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
    url = 'http://www.mmjpg.com'
    pic_urls = []
    res = requests.get(url, headers=headers).text.encode('ISO 8859-1').decode('utf-8')
    soup = BeautifulSoup(res, 'lxml')
    urls = soup.select('body > div.main > div.pic > ul > li > span.title > a')
    for url in urls:
        data = {}
        title = url.string
        pic_id = url.get('href').split('/')[-1]
        data['title'] = title
        data['pic_num'] = pic_id
        pic_urls.append(data)
    return pic_urls


def pic_data(pic_urls):
    """
    获取ajax请求后返回的图片地址数据
    :param pic_urls: 带有图片集编号的list
    :return: 带有图片地址数据的list
    """
    url_list = []
    for url in pic_urls:
        data = {}
        pic_num = url['pic_num']
        headers = {
            'Host': 'www.mmjpg.com',
            'Referer': 'http://www.mmjpg.com/mm/' + str(pic_num),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        data['title'] = url['title']
        data['pic_num'] = pic_num
        params = {
            'id': pic_num,
            'page': '8999'
        }
        url = base_url + urlencode(params)
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                res = response.text
                data['pid'] = list(i for i in res.split(','))
                url_list.append(data)
        except requests.ConnectionError as e:
            print('Error', e.args)
    return url_list


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
        pic_num = urls['pic_num']
        url_list = urls['pid']
        pic_url_dict['pic_num'] = pic_num
        if url_list:
            for i in range(1, len(url_list) + 1):
                picUrl = pic_base_url + str(pic_num) + '/' + str(i) + 'i' + url_list[i - 1] + '.jpg'
                pic_urls.append(picUrl)
            pic_url_dict['picurl'] = pic_urls
            pic_urls_list.append(pic_url_dict)
    # print(pic_urls_list)
    return pic_urls_list


def download(pic_url_list):
    """
    根据地址获取图片并下载到本地
    :param pic_url_list: 带有图片完整地址的list
    :return:
    """
    for pic_urls in pic_url_list:
        pic_num = pic_urls['pic_num']
        filename = pic_urls['title']
        header = {
            'Referer': 'http://www.mmjpg.com/mm/' + str(pic_num),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        pic_url = pic_urls['picurl']
        if not os.path.exists(filename):
            os.mkdir(filename)
        for url in pic_url:
            res = requests.get(url, headers=header).content
            # print(res)
            path = filename + '/' + url.split('/')[-1]
            print(path)
            with open(path, 'wb') as f:
                f.write(res)


if __name__ == '__main__':
    url_list = pic_data(pic_num())
    pic_url(url_list)
    download(pic_url(url_list))
