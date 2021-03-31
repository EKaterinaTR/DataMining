import urllib.request
import collections
from urllib.parse import urlparse

import psycopg2
from bs4 import BeautifulSoup, SoupStrainer


def spider(parent, url, deep, graf, url_table, id_table, scheme):
    print(deep)
    if deep > 0:
        deep -= 1
        html = ''
        try:
            html = urllib.request.urlopen(url).read()
        except Exception:
            print(url)

        url_id = get_url_id(url, url_table, id_table, graf);
        if parent != '':
            create_edge(get_url_id(parent, url_table, id_table, graf), url_id, graf)
        if deep > 0 and is_it_new_url(url_id, url_table):
            for link in BeautifulSoup(html, parse_only=SoupStrainer('a')):
                if link.has_attr('href'):
                    spider(url, full_url(link['href'], scheme, urlparse(url).netloc).geturl(), deep, graf,
                           url_table, id_table, scheme)


def full_url(url, u_schceme, u_netloc):
    url = urlparse(url)
    url = url._replace(scheme=u_schceme)
    url = url._replace(fragment='')
    if url.netloc == '':
        url = url._replace(netloc=u_netloc)
    return url


def get_url_id(url, url_table, id_table, graf):
    id = url_table.get(url)
    if id is None:
        id = len(url_table)
        url_table[url] = id
        id_table[id] = url
        add_url_in_graf(id, graf)
    return id


def create_edge(parent_id, child_id, graf):
    counter = graf[parent_id]
    counter[child_id] += 1


def add_url_in_graf(id_url, graf):
    counter = collections.Counter()
    graf[id_url] = counter


def is_it_new_url(url_id, url_table):
    return url_id == len(url_table) - 1


from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def insert_database(connection, query, data):
    records = ", ".join(["%s"] * len(data))
    insert_query = (
            query + f"{records}"
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(insert_query, data)


def create_list(graf):
    list = []
    for node_from in graf:
        for node_to in graf[node_from]:
            list.append((node_from, node_to, graf[node_from][node_to]))
    return list


# main
url = 'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0'
deep = 2
url_table = {}
id_table = {}
graf = {}

spider('', url, deep, graf, url_table, id_table, 'https')

connection = create_connection('postgres', 'postgres', 'data4ril',
                               'database-2.cth6xwztbzlm.us-east-1.rds.amazonaws.com', 5432)
insert_database(connection, "INSERT INTO id_url VALUES", list(id_table.items()))
insert_database(connection, "INSERT INTO graf  VALUES", create_list(graf))
