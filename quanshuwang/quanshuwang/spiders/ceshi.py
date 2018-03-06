import re
url = 'http://www.quanshuwang.com/book_134165.html'
url = re.findall(r"http://www.quanshuwang.com/book_(\d+)",url)
print(url)