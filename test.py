import requests
from bs4 import BeautifulSoup

# http://zjrb.zjol.com.cn/html/2021-01/21/content_3404973.htm?div=-1
# main-article

news_rsp = requests.get('http://paper.people.com.cn/rmrb/html/2021-01/26/nw.D110000renmrb_20210126_1-01.htm')
news_soup = BeautifulSoup(news_rsp.content, 'html.parser')
news_content = str(news_soup.find_all(name='div', attrs={"class": "article"}))
# element = soup.find(name='founder-content')
# print(element)