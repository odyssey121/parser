import urllib.request
from bs4 import BeautifulSoup


class Parser:
    TRY_VALUES = [
        'containerClass', 'containerTag',
        'pageContainer', 'pageContainerСlass',
        'pageCount', 'pageFormat', 'site', 'timeClass',
        'titleClass', 'titleTag'
    ]
    Errors = []

    def __init__(self, data):
        self.values = self.filter(data)

    def filter(self, data):
        filtered = {}
        if type(data) == type({}):
            for key in data:
                if key in self.TRY_VALUES:
                    filtered[key] = data[key] if data[key] else None
            print(filtered)
        else:
            raise 'Type Error Must Only Dict'
        return filtered

    def getHTML(self, url):
        try:
            response = urllib.request.urlopen(url)
        except:
            return self.Errors.append(['Неверный адресс сайта'])
        return response.read()

    def parse(self, html):
        news = []
        tag = self.values['containerTag']
        tagClass = self.values['containerClass']
        tagTitle = self.values['titleTag']
        titleClass = self.values['titleClass']
        timeClass = self.values['timeClass']
        soup = BeautifulSoup(html, 'html.parser')
        for oneConteiner in soup.find_all(tag, {'class': tagClass}):
            try:
                title = oneConteiner.find(tagTitle, {'class': titleClass}).text
            except AttributeError:
                title = 'необнаруженно'

            try:
                date = oneConteiner.find('', {'class': timeClass}).text
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
        pages = []
        try:
            tag = self.values['pageContainer']
            tagClass = self.values['pageContainerСlass']
            soup = BeautifulSoup(html, 'html.parser')
            soup = soup.find(tag, {'class': tagClass})
            for a in soup:
                page = a.text
                pages.append(page) if page.isdigit() else False
        except AttributeError and KeyError:
            return False

        return int(pages[-1])

    def start(self):
        news = []
        site = self.values['site']
        pageFormat = self.values['pageFormat']
        html = self.getHTML(self.values['site'])
        pageCount = int(self.values['pageCount']) if ('pageCount' in self.values and self.values['pageCount'] != None)else self.getTotalPage(
            html)
        if len(self.Errors) != 0:
            return self.Errors
        print(pageCount, '102')
        if pageCount:
            for page in range(1, pageCount+1):
                print('Parsing  %d%%' % (page / pageCount * 100))
                news.extend(
                    self.parse(
                        self.getHTML('{}{}{}'
                                     .format(site, pageFormat, page))))
        else:
            news.extend(
                self.parse(
                    self.getHTML(site)))
        return news


parser = Parser({
    'site': 'https://pasmi.ru/cat/news',
    'pageFormat': "/page/",
    'containerTag': "article",
    'containerClass': 'preview',
    'pageContainer': "div",
    'pageContainerСlass': "nav-links",
    'timeClass': "1time",
    'titleClass': "",
    'titleTag': "",
    'pageCount': "2",
})
print(parser.start())
