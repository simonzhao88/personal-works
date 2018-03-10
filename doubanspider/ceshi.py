from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
request = Request('https://book.douban.com/subject/5958737/?from=tag_all' )
html = urlopen(request).read()
soup = BeautifulSoup(html,"lxml")
author_info =  soup.xpath('//*[@id="info"]/a')

print(author_info)
