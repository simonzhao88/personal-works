from geturls import get_urls
from gethouseinfo import get_house_info

if __name__ == '__main__':
    urls,html = get_urls()
    get_house_info(urls,html)
