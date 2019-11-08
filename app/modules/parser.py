import urllib.request
from bs4 import BeautifulSoup


class Parser:
    
    TRY_VALUES = [
        'containerClass', 'containerTag',
        'pageContainer', 'pageContainerСlass',
        'pageCount', 'pageFormat', 'site', 'timeClass',
        'titleClass', 'titleTag'
    ]

    def __init__(self, data):
        self.values = self.filter(data)

    def filter(self, data):
        filtered = {}
        if type(data) == type({}):
            for value in self.TRY_VALUES:
                if value in data and data[value]:
                    filtered[value] = data[value]
                else:
                    filtered[value] = None
        return filtered

    def getHTML(self, url):
        try:
            response = urllib.request.urlopen(url)
        except:
            return None
        return response.read()

    def parse(self, html):
        news = []
        tag = self.values['containerTag']
        tagClass = self.values['containerClass']
        tagTitle = self.values['titleTag'] if self.values['titleTag'] != None else 'h1'
        titleClass = self.values['titleClass']
        timeClass = self.values['timeClass']
        try:
            soup = BeautifulSoup(html, 'html.parser')
        except TypeError:
            return False
        for oneConteiner in soup.find_all(tag, {'class': tagClass}):
            try:
                title = oneConteiner.find(tagTitle, {'class': titleClass}).text
            except AttributeError:
                title = 'необнаруженно'
            try:
                if timeClass == None:
                    raise AttributeError
                date = oneConteiner.find(None, {'class': timeClass}).text
            except AttributeError:
                date = 'необнаруженно'

            try:
                linkContent = [a.get('href')
                               for a in oneConteiner.find_all('a')]
            except AttributeError:
                linkContent = 'необнаруженно'

            news.append({
                'title': title,
                'date': date,
                'linkContent': linkContent
            })

        return news

    def getTotalPage(self, html):
        userPages = self.values['pageCount']
        if userPages != None:
            return int(userPages)
        else:
            return False
        # else:
        #     pages = []
        #     tag = self.values['pageContainer']
        #     tagClass = self.values['pageContainerСlass']
        #     if tag != None and tagClass != None:
        #         try:
        #             soup = BeautifulSoup(html, 'html.parser')
        #             soup = soup.find(tag, {'class': tagClass})
        #         except TypeError:
        #             return False
        #         for a in soup:
        #             try:
        #                 page = a.text
        #                 pages.append(page) if page.isdigit() else None
        #             except AttributeError:
        #                 continue
        #     return int(pages[-1])

    def start(self):
        news = []
        site = self.values['site']
        pageFormat = self.values['pageFormat']
        html = self.getHTML(self.values['site'])
        totalPages = self.getTotalPage(html)
        try:
            if totalPages:
                for page in range(1, totalPages+1):
                    print('Parsing  %d%%' % (page / totalPages * 100))
                    news.extend(
                        self.parse(
                            self.getHTML('{site}{pageFormat}{page}'
                                         .format(site=site, pageFormat=pageFormat, page=page))))
            else:
                news.extend(
                    self.parse(
                        self.getHTML(site)))
        except TypeError:
            return 'Неверный адресс сайта'

        return news

