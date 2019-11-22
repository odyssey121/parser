from abc import ABC, abstractmethod
from config import connParam
from psycopg2 import sql, connect, errors
from psycopg2.extras import DictCursor

# абстрактный класс для драйверов(парсеров)


class Driver(ABC):
    # лист адрессов которые будем парсить
    SOURCE_LIST = []
    KEY_WORDS = []
    # кортедж новостей фильтрованных новостей
    FILTERED = tuple()

    # проверка по ключевым словам
    @abstractmethod
    def corruptionCheck(self, text):
        pass

    # парсим адресс
    @abstractmethod
    def parse(self, url):
        pass

    # startup logic
    @abstractmethod
    def start(self):
        pass

    # получаем ключивые слова  из бд
    def getKeyWords(self):
        conn = connect(**connParam)
        with conn.cursor() as cursor:
            conn.autocommit = True
            query = sql.SQL("select {0} from {1}").format(
                sql.Identifier('keywords', 'title'), sql.Identifier('keywords'))
            cursor.execute(query.as_string(conn))
            rows = cursor.fetchall()
        self.KEY_WORDS = [row[0] for row in rows]

    # получаем источники из бд по типу
    def getSources(self, kind='youtube'):
        conn = connect(**connParam)
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            conn.autocommit = True
            query = sql.SQL("select {0} from {1} where {2} = {3}").format(
                sql.SQL(', ').join(
                    map(sql.Identifier, ['id', 'name', 'service_link'])),
                sql.Identifier('sources'),
                sql.Identifier('type'),
                sql.Literal(kind)
            )
            cursor.execute(query.as_string(conn))
            self.SOURCE_LIST = [{key: value for key,
                                 value in row.items()} for row in cursor]

    # пишит в бд article принимает словарь как аргумент title link body article_date sourceId
    def insertArticle(self, article):
        try:
            conn = connect(**connParam)
            with conn.cursor() as cursor:
                conn.autocommit = True
                query = sql.SQL("insert into articles ({}) values ({}) on conflict ({}) do nothing").format(
                    sql.SQL(', ').join(map(sql.Identifier, article.keys())),
                    sql.SQL(', ').join(map(sql.Placeholder, article.keys())),
                    sql.SQL(', ').join(map(sql.Identifier, [list(article.keys())[key] for key in [0, 3]])))
                cursor.execute(query.as_string(conn), article)
        except errors.UniqueViolation as error:
            print(error)
    # пишит в бд scan_logs логи

    def insertLog(self, data):
        try:
            conn = connect(**connParam)
            with conn.cursor() as cursor:
                conn.autocommit = True
                query = sql.SQL("insert into scan_logs ({}) values ({})").format(
                    sql.SQL(', ').join(map(sql.Identifier, data.keys())),
                    sql.SQL(', ').join(map(sql.Placeholder, data.keys())))
                cursor.execute(query.as_string(conn), data)
        except errors.UniqueViolation as error:
            print(error)
