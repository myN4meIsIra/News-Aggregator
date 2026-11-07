# news title
'''
    object to hold news stories/entries which all are basically the same topic
'''

from cust_logging.logger import Log
Log = Log('History_of_News_Entry.py')


class History_of_News_Entry():
    def __init__(self,  title, url, body, date):
        self.title = title
        self.url = url
        self.body = body
        self.date = date


    # getter
    def get(self):
        return {
                'title':self.title,
                'url':self.url,
                'body':self.body,
                'date':self.date
            }

