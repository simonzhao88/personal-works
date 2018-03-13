from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
request = Request('https://book.douban.com/subject/2035179/?from=tag_all' )
html = urlopen(request).read().decode('utf-8')
# print(html)
author_infos = BeautifulSoup(html,'lxml')
# print(author_infos)
author_info = author_infos.select('#info > a')
j = author_info[0].get_text()
print(j)
for xx in j:
    i = xx.get_text()
print(i)
# print(author_info)
