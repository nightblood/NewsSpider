from _datetime import datetime
import json

import requests
from bs4 import BeautifulSoup
import sqlite3

# http://zjrb.zjol.com.cn/html/2021-01/21/content_3404973.htm?div=-1
# main-article

# news_rsp = requests.get('http://paper.people.com.cn/rmrb/html/2021-01/26/nw.D110000renmrb_20210126_1-01.htm')
# news_soup = BeautifulSoup(news_rsp.content, 'html.parser')
# news_content = str(news_soup.find_all(name='div', attrs={"class": "article"}))
# element = soup.find(name='founder-content')
# print(element)


# con = sqlite3.connect('spider.sqlite')
# cursor = con.cursor()
# cursor.execute('create table if not exists tb_record(id int not null auto_increment, content varchar(100));')
# con.commit()
# cursor.execute("insert into tb_record (content) values ('abcd test')")
# con.commit()
# con.close()

class Test(object):
    a = 'a'
    b = 'b'

    def __init__(self):
        c = 'c'


def MyJsonEncoder(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, Test):
        return {'a':obj.a,'b':obj.b}
    else:
        raise TypeError('%r is not JSON serializable' % obj)


if __name__ == '__main__':
    t = Test()
    s = json.dumps(t, ensure_ascii=False, default=MyJsonEncoder)
    print(s)
