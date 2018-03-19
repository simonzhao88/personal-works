import threading
from urllib.request import urlopen
from urllib.request import Request
import random
from bs4 import BeautifulSoup
import http.client
from urllib import error


lock = threading.Lock()
readfile = open('proxy.txt','w+')
writefile = open('useful.txt', 'w')
start_url = "http://www.xicidaili.com/nn/"
def getProxy_list(start_url):
    headers = [{'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"},
              {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.27 Safari/537.36"}]
    data = None
    proxyFile = open('proxy.txt', 'a')
    for page in range(1, 500):
        url = start_url + str(page)
        try:
            response = Request(url, data, headers=headers[random.randint(0, 1)])
            res = urlopen(response).read()
            soup = BeautifulSoup(res, 'lxml')
        except (error.HTTPError, error.URLError) as e:
            print(e)
            continue
        trs = soup.find('table', id='ip_list').find_all('tr')
        # print(trs)
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            print(ip, port)
            proxyFile.write('%s|%s\n' % (ip, port))
    proxyFile.close()

def getUsefulIp():
    url = 'http://www.baidu.com/'
    hearders = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.27 Safari/537.36"}
    while 1:
        lock.acquire()
        ll = readfile.readline().strip()
        lock.release()
        if len(ll) == 0:
            break
        line = ll.strip().split('|')
        ip = line[0]
        port = line[1]

        try:
            conn = http.client.HTTPConnection(ip, port, timeout=5.0)
            conn.request('GET', url, hearders=hearders)
            res =conn.getresponse()
            lock.acquire()
            print('+++success:'+ip+':'+port)
            writefile.write(ll+"\n")
            lock.release()
        except:
            print('+++failure:'+ip+':'+port)
if __name__=='__main__':
    tmp = open('proxy.txt', 'w')
    tmp.write("")
    tmp.close()
    getProxy_list(start_url)
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=getUsefulIp)
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()

    readfile.close()
    writefile.close()
