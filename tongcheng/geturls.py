from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib import error
from urllib.request import Request
import random
import time
import numpy as np


headers = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
m = int(input("请输入要爬取的页数："))
# m = 1
urls = []
htmls = []
data = {
    'Cookie':'f=n; userid360_xml=4744FC32B38F45E155EB322584D04F99; time_create=1523544907564; f=n; suid=3178340640; f=n; id58=c5/njVp6ay4FSYb7C8pIAg==; wmda_uuid=e283147989c6b89504e4b5e0031f467b; wmda_new_uuid=1; wmda_visited_projects=%3B2385390625025; als=0; myfeet_tooltip=end; commontopbar_myfeet_tooltip=end; city=cd; 58home=cd; commontopbar_ipcity=cd%7C%E6%88%90%E9%83%BD%7C0; defraudName=defraud; ppStore_fingerprint=3D00F1958814FEC3327BCA380FC067D134BCABE49BCBBFE4%EF%BC%BF1521011767997; commontopbar_new_city_info=102%7C%E6%88%90%E9%83%BD%7Ccd; 58tj_uuid=12b10551-fb8b-4f20-bdde-53b7358e49ff; new_session=0; new_uv=9; utm_source=; spm=; init_refer=http%253A%252F%252Fcd.58.com%252Fzufang%252Fsub%252Fl20%252Fs2285_2286%252Fj3%252F%253Fminprice%253D0_2500; wmda_session_id_2385390625025=1521006817042-fbda2903-a589-1eec; f=n; xxzl_deviceid=JlNRAqWvm%2Bk5h9m0MyyNT89rAol5SWQMs5PGupXs%2FteikjA21jbu4tOmsPSHOgGv',
    'Host':'cd.58.com'
}
#获取网址
def get_urls():
    for page_num in range(1,m+1):
        start_url = 'http://cd.58.com/zufang/sub/l20/s2285_2286/j3/pn' + str(page_num) + '/?minprice=0_2500'
        # print(start_url)
        time.sleep(np.random.rand() * 5)
        try:
            res = Request(start_url,headers=headers[random.randint(0,2)])
            response = urlopen(res)
            html = BeautifulSoup(response,'lxml')
        except (error.HTTPError, error.URLError) as e:
            print(e,'1')
            continue
        url_list = html.select('body > div.mainbox > div.main > div.content > div.listBox > ul > li > div.des > h2 > a')
        for i in url_list:
            url = i.get('href')
            urls.append(url)
        htmls.append(html)
    return urls
