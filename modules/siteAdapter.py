import os.path
import sys
from sourceParser.findFeed import findFeed
from template import Driver
import datetime
import lxml.html
from dateutil import parser as dp
import re
import requests
from bs4 import BeautifulSoup as bs4
import feedparser


class RssParser(Driver):
    # RSS_LIST = []
    FILTERED = tuple()

    def __init__(self, saveDb=True):
        self.saveDb = saveDb
        self.getKeyWords()
        self.getSources(kind='site')
        # self.getListRssFromUrlList()

    # def getListRssFromUrlList(self):
    #     self.RSS_LIST = [{key: (findFeed(val) if key != 'id' else val) for key, val in item.items()}
    #                      for item in self.SOURCE_LIST]

    def corruptionCheck(self, text):
        return any(key in text.lower() for key in self.KEY_WORDS)

    def parse(self, item):
        url = item.get('service_link', None)
        sourceId = item.get('id', None)
        saveDb = self.saveDb
        f = None
        try:
            f = feedparser.parse(url)
            if len(f['entries']) is 0:
                self.insertLog({
                    'status': 'not found',
                    'description': str(f['bozo_exception']),
                    'sourceId': sourceId
                })
        except Exception as error:
            self.insertLog({
                'status': 'error',
                'description': error,
                'sourceId': sourceId})

        for entry in f['entries']:
            title = entry.get('title', 'не определено')
            link = entry.get('link', 'не определено')
            published = entry.get('published', 'не определено')
            summary = entry.get('summary', 'не определено')
            if(self.corruptionCheck(title) or self.corruptionCheck(summary)):
                if saveDb:
                    self.insertArticle({
                        'title': title,
                        'link': link,
                        'body': lxml.html.fromstring(summary).text_content().replace(u'\xa0', ' '),
                        'article_date': dp.parse(published).isoformat(),
                        'sourceId': sourceId,
                    })
                else:
                    self.FILTERED += ({
                        'title': title,
                        'link': link,
                        'body': lxml.html.fromstring(summary).text_content().replace(u'\xa0', ' '),
                        'article_date': dp.parse(published).isoformat(),
                        'sourceId': sourceId,
                    },)

    def start(self):
        for item in self.SOURCE_LIST:
            self.parse(item)
        return self.FILTERED


if __name__ == '__main__':
    parser = RssParser()
    result = parser.start()
