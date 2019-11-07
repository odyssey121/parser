import urllib.request
from bs4 import BeautifulSoup

BASE_URL = 'https://pasmi.ru/cat/news'
PAGE_PARAMS = {1: '/page/', 2: '?page='}
BASE_CONTAINER_PARAMS = {
    'container': {'tag': 'article', 'class': 'preview'},
    'title': {'tag': 'h1', 'class': None},
    'pages': {'tag': 'div', 'class': 'nav-links'}
}



def askYesNo(question):
    response = None
    while response not in ('y', 'n'):
        response = input(question).lower()
    return True if response == 'y' else False


def askNumber(question, low=1, high=3):
    response = None
    while response not in range(low, high):
        try:
            response = int(input(question))
        except:
            continue
    return response


def getParams():
    # CUSTOM = False
    # print('''\t\t\t
    # Доброго времени суток Вас приветсвует Простой парсер Новостей или Блогов!\n
    # Ответьте пожалуйста на пару простых вопросов.
    # ''')
    # if (askYesNo('будем парсить сайт {} \t(y/n)? : '.format(BASE_URL)) == False):
    #     CUSTOM = True
    #     CUSTOM_URL = input(
    #         'Введите полное название сайта например => "https://www.gazeta.ru/news" без слеша в конце!: ')
    #     BASE_CONTAINER_PARAMS['pages']['tag'] = input(
    #         'Укажите тэг контейнер в котором лежаты сслыки на страницы <a>number</a>  "span/div/section и т.д  или ничего не вводите если нету : ')
    #     BASE_CONTAINER_PARAMS['pages']['class'] = input(
    #         'Укажите класс тэга для страниц или ничего не вводите если нету "h1/h2/h3 и т.д :')
    #     try:
    #         PAGE_TOTAL = totalPage(
    #             getHTML(CUSTOM_URL), CUSTOM_CONTAINER_PARAMS)
    #         PAGE_COUNT = askNumber(
    #             'Найдено всего = {} страниц. Скоко будем парсить?? : '.format(str(PAGE_TOTAL)), 1, PAGE_TOTAL)
    #     except:
    #         PAGE_COUNT = None

    #     CUSTOM_PAGE_PARAMS = PAGE_PARAMS[(askNumber(
    #         'Какой формат url страниц? если {} нажмите 1 , а если {} нажмите 2 : '.format(PAGE_PARAMS[1], PAGE_PARAMS[2])))]
    #     BASE_CONTAINER_PARAMS['container']['tag'] = input(
    #         'Укажите тэг - контейнера 1 новости "div/article и тд" : ')
    #     BASE_CONTAINER_PARAMS['container']['class'] = input(
    #         'Укажите class - этого Тэга или ничего не вводите если нету : ')
    #     BASE_CONTAINER_PARAMS['title']['tag'] = input(
    #         'Укажите тэг заголовка новости "h1/h2/h3 и т.д :')
    #     BASE_CONTAINER_PARAMS['title']['class'] = input(
    #         'Укажите класс заголовка новости или ничего не вводите если нету  :')
    # else:
    #     PAGE_TOTAL = totalPage(getHTML(BASE_URL))
    #     PAGE_COUNT = askNumber(
    #         'Найдено всего = {} страниц. Скоко будем парсить?? : '.format(str(PAGE_TOTAL)), 1, PAGE_TOTAL)

    return {
        'urlForParse': 'https://pasmi.ru/cat/news',
        'pageCount': 10,
        'pageParam': PAGE_PARAMS[1],
        'containerParam': BASE_CONTAINER_PARAMS,
    }


def getHTML(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html, options=BASE_CONTAINER_PARAMS):
    news = []
    containerTag = options['container']['tag']
    containerClass = options['container']['class']
    titleTag = options['title']['tag']
    titleClass = options['title']['class']
    soup = BeautifulSoup(html, 'html.parser')

    for oneConteiner in soup.find_all(containerTag, {'class': containerClass}):
        try:
            title = oneConteiner.find(titleTag, {'class': titleClass}).text
            try:
                date = oneConteiner.find('span', {'class': 'time'}).text
            except:
                date = 'null'

            linkContent = [a.get('href') for a in oneConteiner.find_all('a')]
            news.append({'title': title, 'date': date,
                         'linkContent': linkContent})
        except:
            print('someThing wrong')

    return news


def totalPage(html, options=BASE_CONTAINER_PARAMS):
    tag = options['pages']['tag']
    tagClass = options['pages']['class']
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find(tag, {'class': tagClass})
    pages = []

    for a in soup:
        try:
            page = a.text
            pages.append(page) if page.isdigit() else None
        except AttributeError:
            continue
    return int(pages[-1])


def save(newsList, path):
    with open(path, 'w', encoding='utf-8') as write_file:
        write_file.write(HTML)
        for count, element in enumerate(newsList):
            write_file.write(
                '''<div class='container'>
                    <span>{index}</span>
                    <h3>{title}<h3>
                    {date}
                    <div>{links}</div>
                    </div>'''.format(
                    title=element['title'], date=element['date'],
                    index=count, links=element['linkContent']
                ))
    print('Готово новости сохранены в ./index.html')


def main():
    OPTIONS = getParams()
    all_news = []
    if type(OPTIONS['pageCount']) == int:
        for page in range(1, OPTIONS['pageCount'] + 1):
            print('Parsing  %d%%' % (page / OPTIONS['pageCount'] * 100))
            all_news.extend(
                parse(getHTML('{}{}{}'.format(
                    OPTIONS['urlForParse'], OPTIONS['pageParam'], page)
                )))
    else:
        all_news.extend(parse(getHTML(OPTIONS['urlForParse']),
                              OPTIONS['containerParam']))

    return all_news


if __name__ == '__main__':
    main()
