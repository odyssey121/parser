from config import connParam
from psycopg2 import sql, connect, errors
from psycopg2.extras import DictCursor


def insertArticle(article):
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


def insertKeyWord(title):
    conn = connect(**connParam)
    with conn.cursor() as cursor:
        conn.autocommit = True
        query = sql.SQL("insert into keywords ({}) values ({})").format(
            sql.Identifier('title'),
        )
        cursor.execute(query.as_string(conn))


def getKeyWords():
    conn = connect(**connParam)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        conn.autocommit = True
        query = sql.SQL("select {0} from {1}").format(
            sql.Identifier('keywords', 'title'), sql.Identifier('keywords'))
        cursor.execute(query.as_string(conn))
        rows = cursor.fetchall()

    return [row[0] for row in rows]


def getSources(kind='site'):
    conn = connect(**connParam)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        conn.autocommit = True
        query = sql.SQL("select {0} from {1} where {2} = {3}").format(
            sql.SQL(', ').join(map(sql.Identifier, ['id', 'name'])),
            sql.Identifier('sources'),
            sql.Identifier('type'),
            sql.Literal(kind)
        )
        cursor.execute(query.as_string(conn))
        # rows = cursor.fetchall()
        return [{key: value for key, value in row.items()} for row in cursor]

    # return rows


def getSourceByName(name):
    conn = connect(**connParam)
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        conn.autocommit = True
        query = sql.SQL("select {0} from {1} where {2} = {3}").format(
            sql.SQL(', ').join(map(sql.Identifier, ['id', 'name'])),
            sql.Identifier('sources'),
            sql.Identifier('name'),
            sql.Literal(name)
        )
        cursor.execute(query.as_string(conn))
        # rows = cursor.fetchall()
        return [{key: value for key, value in row.items()} for row in cursor]


def insertSource(source):
    try:
        conn = connect(**connParam)
        with conn.cursor() as cursor:
            conn.autocommit = True
            query = sql.SQL("insert into sources ({}) values ({}) returning id").format(
                sql.SQL(', ').join(map(sql.Identifier, source.keys())),
                sql.SQL(', ').join(map(sql.Placeholder, source.keys())))
            cursor.execute(query.as_string(conn), source)
            return cursor.fetchone()[0]

    except errors.UniqueViolation as error:
        print(error)



