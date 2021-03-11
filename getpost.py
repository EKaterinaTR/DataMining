import psycopg2
import requests
import collections


# counting words from vk posts

def count_unique_words(text, counter):
    words = text.split()
    for word in words:
        counter[word] += 1


def get_wall_date(domain, v, access_token, count, offset):
    return requests.get("https://api.vk.com/method/wall.get",
                        params={
                            'domain': domain,
                            'v': v,
                            'access_token': access_token,
                            'count': count,
                            'offset': offset
                        }
                        )


def get_counter_with_unique_words_from_wall(domain, v, access_token, count, offset):
    the_limit = 100
    main_counter = collections.Counter()
    while count > 0:
        response = get_wall_date(domain, v, access_token, count, offset)
        date = response.json()['response']
        items = date['items']
        for item in items:
            count_unique_words(item['text'], main_counter)
            if 'copy_history' in item:
                count_unique_words(item['copy_history'][0]['text'], main_counter)
        count -= the_limit
        offset += the_limit
    return main_counter


# working with rds
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


#main
domain = 'itis_kfu'
v = 5.52
access_token = '28b9b30a28b9b30a28b9b30a5c28cbacbd228b928b9b30a7671a6a67c3c67ea3ceda9df'
count = 200
offset = 0

counter = get_counter_with_unique_words_from_wall(domain, v, access_token, count, offset).most_common()

connection = create_connection('postgres', 'postgres', 'data4ril',
                               'database-2.cth6xwztbzlm.us-east-1.rds.amazonaws.com', 5432)
insert_database(connection, "INSERT INTO words VALUES", counter)
