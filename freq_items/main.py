# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import csv
from csv import Dialect
import collections


def get_frequent_items(support, source, hash_function_1, hash_function_2):
    # first step
    items = {}
    singelton = collections.Counter()
    hashtable_1 = collections.Counter()
    hashtable_2 = collections.Counter()
    freq_item = set()

    count_singlton(source, items, singelton)
    count_first_hashtable(source, support, items, singelton, hash_function_1, hashtable_1)
    count_second_hashtable(source, support, items, singelton, hash_function_1, hashtable_1, hash_function_2,
                           hashtable_2)
    freq_items(source, support, items, singelton, hash_function_2, hashtable_2, freq_item)

    return freq_item


def count_singlton(source, items, singelton):
    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            sc = row['StockCode']
            if not (sc in items):
                items[sc] = len(items)
            singelton[items[sc]] += 1


def count_first_hashtable(source, support, items, singelton, hashfunction, hashtable_1):
    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        last_invoice_no = 0
        bucket = []

        for row in reader:
            new_invoice_no = row['InvoiceNo']
            new_item = items[row['StockCode']]

            if new_invoice_no != last_invoice_no:
                last_invoice_no = new_invoice_no
                bucket = []

            if singelton[new_item] >= support:
                for item in bucket:
                    if item > new_item:
                        hashtable_1[hashfunction(new_item, item, len(singelton))] += 1
                    else:
                        hashtable_1[hashfunction(item, new_item, len(singelton))] += 1
                bucket.append(new_item)


def count_second_hashtable(source, support, items, singelton, hashfunction_1, hashtable_1, hashfunction_2, hashtable_2):
    with open(source, newline='') as csvfile:

        reader = csv.DictReader(csvfile)
        last_invoice_no = 0
        bucket = []

        for row in reader:
            new_invoice_no = row['InvoiceNo']
            new_item = items[row['StockCode']]

            if new_invoice_no != last_invoice_no:
                last_invoice_no = new_invoice_no
                bucket = []

            if singelton[new_item] >= support:
                for item in bucket:

                    if item > new_item and hashtable_1[hashfunction_1(new_item, item, len(singelton))] >= support:
                        hashtable_2[hashfunction_2(new_item, item, len(singelton))] += 1
                    if item <= new_item and hashtable_1[hashfunction_1(item, new_item, len(singelton))] >= support:
                        hashtable_2[hashfunction_2(item, new_item, len(singelton))] += 1
                bucket.append(new_item)


def freq_items(source, support, items, singelton, hashfunction_2, hashtable_2, freq_item):
    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        last_invoice_no = 0
        bucket = []

        for row in reader:
            new_invoice_no = row['InvoiceNo']
            stock_code = row['StockCode']
            new_item = items[stock_code]

            if new_invoice_no != last_invoice_no:
                last_invoice_no = new_invoice_no
                bucket = []

            if singelton[new_item] >= support:
                freq_item.add(stock_code)
                for stock_code_in_b in bucket:
                    item = items[stock_code_in_b]
                    if item > new_item and hashtable_2[hashfunction_2(new_item, item, len(singelton))] >= support:
                        freq_item.add((stock_code, stock_code_in_b))
                    if item <= new_item and hashtable_2[hashfunction_2(item, new_item, len(singelton))] >= support:
                        freq_item.add((stock_code_in_b, stock_code))

                bucket.append(stock_code)


def hash_function(a, x, b, y, mod):
    return (a * int(x) + int(b) * y) % mod


def count_number_of_buckets(source):
    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        last_invoice_no = 0
        number = 0

        for row in reader:
            new_invoice_no = row['InvoiceNo']
            if new_invoice_no != last_invoice_no:
                last_invoice_no = new_invoice_no
                number += 1

        return number


def get_description(source, items):
    with open(source, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        description = {}

        for row in reader:
            code = row['StockCode']
            if code in items:
                description[code] = row['Description']

        return description


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    def h_f_1(x, y, mod):
        return hash_function(1, x, 1, y, mod)


    def h_f_2(x, y, mod):
        return hash_function(2, x, 1, y, mod)
    source = 'data/data_some_part.csv'
    f_i = get_frequent_items(78, source, h_f_1, h_f_2)
    print(f_i)
    print(get_description(source, f_i))
    print(count_number_of_buckets(source))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
