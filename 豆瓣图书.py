import requests
from bs4 import BeautifulSoup
import json
from book_info import BookInfo
import sqlite3
from flask import Flask, request, jsonify, abort
from flask.json import JSONEncoder as _JSONEncoder
import chardet


def MyJsonEncoder(obj):
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, BookInfo):
        author = []
        for item in obj.author:
            author.append({'type': item.type, 'name': item.name})
        return {
                'context': obj.context,
                'type': obj.type,
                'name': obj.name,
                'workExample': obj.workExample,
                'author': author,
                'url': obj.url,
                'isbn': obj.isbn,
                'sameAs': obj.sameAs,
                'imgUrl': obj.imgUrl
        }
    else:
        raise TypeError('%r is not JSON serializable' % obj)


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
conn = sqlite3.connect("./book_man.db", check_same_thread=False)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}


def getBookByIsbn(isbn):
    r = requests.get('http://douban.com/isbn/{0}/'.format(isbn), headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    soup.prettify()
    if str(soup.select('title')[0].contents[0]).__contains__('豆瓣错误'):
        return None
    tag_book_info = soup.select('script[type="application/ld+json"]')[0]
    tag_book_img = soup.select('a[class="nbg"]')[0]
    book_info = BookInfo.decode(json.loads(str(tag_book_info.contents[0])))
    book_info.imgUrl = tag_book_img.contents[1].attrs['src']
    return book_info


def saveBook(book):
    conn.execute('''create table if not exists book_info(
                    isbn varchar(100) not null
                    , context varchar(100)
                    ,type varchar(30)
                    , workExample varchar(100)
                    , name varchar(100)
                    , url varchar(100)
                    , sameAs varchar(100)
                    , imgUrl varchar(100)
                    , CONSTRAINT pk_book_info primary key(isbn));''')
    conn.execute('''create table if not exists author_info(
                    isbn varchar(100) not null
                    , type varchar(30)
                    , name varchar(100)
                    )''')
    sql = 'insert into book_info (isbn,context, type, workExample, name, url, sameAs, imgUrl) values("{}","{}","{}","{}","{}","{}","{}","{}");'\
        .format(book.isbn, book.context, book.type, book.workExample, book.name, book.url, book.sameAs, book.imgUrl)
    conn.execute(sql)
    for item in book.author:
        sql = 'insert into author_info (isbn, type, name) values("{}","{}","{}")'.format(book.isbn, item.type, item.name)
        conn.execute(sql)
    conn.commit()


def select_book_by_isbn(isbn):
    sql = 'select * from book_info where isbn="{}"'.format(isbn)
    cur = conn.execute(sql)
    book_info = cur.fetchone()
    sql = 'select * from author_info where isbn="{}"'.format(isbn)
    cur = conn.execute(sql)
    author_info = cur.fetchall()
    # print(author_info)
    cur.close()
    return book_info, author_info


@app.route('/bookman/api/v1/books/', methods=['GET'])
def get_book():
    isbn = request.args.get('isbn')
    book_info, author_info = select_book_by_isbn(isbn)
    if book_info is not None:
        author = []
        for item in author_info:
            author.append({'isbn': item[0], 'type': item[1], 'name': item[2]})
        return jsonify({
            'status': 0,
            'context': book_info[1],
            'type': book_info[2],
            'name': book_info[4],
            'workExample': book_info[3],
            'author': author,
            'url': book_info[5],
            'isbn': book_info[0],
            'sameAs': book_info[6],
            'imgUrl': book_info[7]
        })

    book = getBookByIsbn(isbn)
    if book is None:
        return jsonify({'status': 1, 'desc': '查无此书！！'})
    saveBook(book)
    author = []
    for item in book.author:
        author.append({'type': item.type, 'name': item.name})
    return jsonify({
        'status': 0,
        'context': book.context,
        'type': book.type,
        'name': book.name,
        'workExample': book.workExample,
        'author': author,
        'url': book.url,
        'isbn': book.isbn,
        'sameAs': book.sameAs,
        'imgUrl': book.imgUrl
    })


if __name__ == '__main__':

    # book = getBookByIsbn('97870200087281')
    app.run(debug=True)
    print('end...')
