import requests
from bs4 import BeautifulSoup
import datetime
from openpyxl import load_workbook, Workbook
from os import path


def rmrb(start_dt=datetime.datetime.now().strftime('%Y-%m/%d'), end_dt=datetime.datetime.now().strftime('%Y-%m/%d'), key_words=''):
    '''
    搜索日期从 start_dt 到 end_dt的新闻标题中有 key_words的新闻
    :param start_dt:
    :param end_dt:
    :param key_words:
    :return:
    '''
    base_url = 'http://paper.people.com.cn/rmrb/html/'
    news_dt = start_dt
    today = datetime.datetime.now().strftime('%Y%m%d')
    file = '新闻{0}.xlsx'.format(today)
    if path.exists(file):
        wb = load_workbook(file)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active

    while news_dt <= end_dt:
        for idx in range(1, 21):
            try:
                # 20 个板块链接
                url_panel = '{2}{1}/nbs.D110000renmrb_{0}.htm'.format(str(idx).zfill(2), news_dt, base_url)
                r = requests.get(url_panel)
                soup = BeautifulSoup(r.content, 'html.parser')
                a_tags = soup.find_all('a')
                for item in a_tags:
                    if item.attrs['href'][:3] == 'nw.' and item.contents[0].__contains__(key_words):
                        news_url = '{2}{1}/{0}'.format(item.attrs.get('href'), news_dt, base_url)
                        new_title = item.contents[0]
                        news_rsp = requests.get(news_url)
                        news_soup = BeautifulSoup(news_rsp.content, 'html.parser')
                        news_content = str(news_soup.find_all(name='div', attrs={"class": "article"}))
                        if news_content.__contains__(key_words):
                            ws.append((news_url, new_title))
            except Exception as e:
                pass
        d = datetime.datetime.strptime(news_dt, '%Y-%m/%d')
        news_dt = (d + datetime.timedelta(days=1)).strftime('%Y-%m/%d')
        wb.save(file)
        wb.close()


if __name__ == '__main__':
    start_dt = '2021-01/18'  # 2021-01/19
    end_dt = '2021-01/19'
    key_words = '的'
    rmrb(start_dt, end_dt, key_words)
