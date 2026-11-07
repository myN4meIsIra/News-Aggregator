# news source
'''
    contain news source class
'''

from news_parser import news_parser
from cust_logging.logger import Log
log = Log("News_Source.py")

class News_Source():
    def __init__(self, source):
        self.src = source

        # definitions
        self.bozo = None
        self.entries = None
        self.feed = None
        self.headers = None
        self.etag = None
        self.href = None
        self.status = None
        self.encoding = None
        self.bozo_exception = None
        self.version = None
        self.namespaces = None

        self.populate()


    # getter
    '''
        getter
    '''
    def get(self):
        return {
            #'bozo': self.bozo,
            'entries': self.entries,
            #'feed': self.feed,
            #'headers': self.headers,
            #'etag': self.etag,
            #'href': self.href,
            #'status': self.status,
            #'encodings': self.encoding,
            #'bozo_exception': self.bozo_exception,
            #'version': self.version,
            #'namespaces': self.namespaces
        }



    # populate
    '''
        populate the fields
    '''
    def populate(self):
        try:
            src = news_parser(self.src)
            #print(f'{src.entries[0].keys()}')
            #self.bozo = src.bozo
            self.entries = [{"title":entry.title, 'url':entry.link, 'published':entry.published}  for entry in src.entries]      # make entries just a {"title":<>, "url":<>} entry
            #self.feed = src.feed            # todo add feed class
            #self.headers = src.headers
            #self.etag = src.etag
            #self.href = src.href
            #self.status = src.status
            #self.encoding = src.encoding
            #self.bozo_exception = src.bozo_exception
            #self.version = src.version
            #self.namespaces = src.namespaces

        except Exception as E:
            log.error(f"ERROR {E}")

        return self.get()
