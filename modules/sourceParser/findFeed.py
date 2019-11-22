from sys import argv
import requests
from bs4 import BeautifulSoup as bs4
import feedparser
import re
import urllib.parse
import json

regexHttpStart = re.compile(
    r'^(?:http)s?://', re.IGNORECASE)


def getDomain(url):
    # requires 'http://' or 'https://'
    #pat = r'(https?):\/\/(\w+\.)*(?P<domain>\w+)\.(\w+)(\/.*)?'
    #'http://' or 'https://' is optional
    pat = r'((https?):\/\/)?(\w+\.)*(?P<domain>\w+)\.(?P<tail>\w+)(\/.*)?'
    m = re.match(pat, url)
    if m:
        domain = 'http://www.{}.{}'.format(m.group('domain'),m.group('tail'))
        return domain
    else:
        return False


def normalizeUrl(url):
    return url if re.match(regexHttpStart, url) is not None else '{}{}'.format(
        'http://', url
    )


def normalizeFeed(url, href):
    feed = None

    if re.match(regexHttpStart, href) is not None:
        feed = href
    else:
        if href.startswith('//'):
            feed = '{}{}'.format('http:', href)
        else:
            feed = '{}{}'.format(getDomain(url), href)
    return feed

# возвращает рсс или ошибку
# 'rss/xml не найден' если неполучилось найти рсс
# def stepTwo(feedUrl):
#     result = []
#     try:
#         raw = requests.get(feedUrl).text
#         html = bs4(raw, 'html.parser')
#         feedUrls = html.findAll("link", rel="alternate")
#         passibleFeeds = []
#         # print(feedUrls)
#         for f in feedUrls:
#             t = f.get("type", None)
#             if t:
#                 if "rss" in t or "xml" in t:
#                     href = f.get("href", None)
#                     if href:
#                         passibleFeeds.append(href)

#         aTags = html.findAll('a')

#         for a in aTags:
#             href = a.get('href', None)
#             if href:
#                 if "xml" in href or "rss" in href or "feed" in href:
#                     passibleFeeds.append(href)

#         for passible in list(set(passibleFeeds)):
#             normalize = normalizeUrl(passible)
#             f = feedparser.parse(normalize)
#             if len(f.entries) > 0:
#                 if normalize not in result:
#                     result.append(normalize)

#     except Exception as error:
#         print(error)
#     return result


def findFeed(name):
    url = normalizeUrl(name)
    result = []
    try:
        raw = requests.get(url).text
        aptFeeds = []
        html = bs4(raw, 'html.parser')
        feedUrls = html.findAll("link", rel="alternate")
        # print(feedUrls)
        for f in feedUrls:
            t = f.get("type", None)
            if t:
                if "rss" in t or "xml" in t:
                    href = f.get("href", None)
                    if href:
                        feed = normalizeFeed(url, href)
                        aptFeeds.append(feed)

        aTags = html.findAll('a')

        for a in aTags:
            href = a.get('href', None)
            if href:
                if "xml" in href or "rss" in href or "feed" in href:
                    aptFeeds.append(href)

        for aptFeed in list(set(aptFeeds)):
            normFeed = normalizeFeed(url, aptFeed)
            f = feedparser.parse(normFeed)
            if len(f.entries) > 0:
                if normFeed not in result:
                    result.append(normFeed)

    except Exception as error:
        print(error)

    return result


if __name__ == '__main__':
    if len(argv) == 2:
        print(findFeed(argv[1]))

    else:
        print(findFeed('https://reorga.ru/'))
