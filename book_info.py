
class BookInfo(object):
    context = ''
    type = ''
    workExample = ''
    name = ''
    author = []
    url = ''
    isbn = ''
    sameAs = ''
    imgUrl = ''

    def __init__(self):
        self.context = ''
        self.type = ''
        self.workExample = ''
        self.name = ''
        self.author = []
        self.url = ''
        self.isbn = ''
        self.sameAs = ''
        self.imgUrl = ''

    @staticmethod
    def decode(jsonObj):
        book_info = BookInfo()
        book_info.context = jsonObj.get('@context')
        book_info.type = jsonObj.get('@type')
        book_info.workExample = jsonObj.get('workExample')
        book_info.name = jsonObj.get('name')
        book_info.url = jsonObj.get('url')
        book_info.isbn = jsonObj.get('isbn')
        book_info.sameAs = jsonObj.get('sameAs')
        author_list = jsonObj.get('author')
        for item in author_list:
            author = Author()
            author.type = item.get('@type')
            author.name = item.get('name')
            book_info.author.append(author)

        return book_info


class Author(object):
    type = ''
    name = ''

    def __init__(self):
        self.type = ''
        self.name = ''

    def keys(self):
        return ['type', 'name']

    def __getitem__(self, item):
        return getattr(self, item)
