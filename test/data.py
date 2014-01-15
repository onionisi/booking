# coding=utf8
from pymongo import MongoClient
import sys
import time


class Catalog:
    def __init__(self):
        self.key = [ "category", "tag", "cost", "encode" ]

        client = MongoClient('localhost', 27017)
        self.collect = client.test.catalog

    def create(self, files):
        # abandon old one
        self.collect.drop()

        serial_num = 1
        for line in open(files).readlines():
            line_list = line.split()
            line_list[1].decode('utf8').encode(sys.getfilesystemencoding())
            line_list[2] = int(linelist[2])
            line_list.append(serial_num)
            self.collect.insert(dict(zip(self.key, line_list)))
            serial_num += 1

    def find(self, cond):
        # cond form {'filter_key': encode}
        if 'tag' in cond:
            query = {'encode': cond['tag']}
            return self.collect.find_one(query)['tag']
        elif 'encode' in cond:
            query = {'tag': cond['encode']}
            return self.collect.find_one(query)['tag']
        elif 'cost' in cond:
            query = {'tag': cond['cost']}
            return self.collect.find_one(query)['cost']
        elif 'category' in cond:
            query = {'tag': cond['category']}
            return self.collect.find_one(query)['category']
        else:
            pass

class Bill:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.collect = client.test.bills

        self.key = [ "unit", "time", "account", "items" ]
        self.unfinish = {'time.finish': { '$exitsts': False }}

        self.handle = { 'create': self.create,
                        'read': self.read,
                        'update': self.update,
                        'delete': self.delete,
                        'checkout': self.checkout }

        self.cate = Catalog()

    def findall(self, cond):
        # cond form {'filter_key': top_number}
        # all of this is statistic, always return a list

        # condition = {$lg $lt}
        result = []

        # units book(no items)
        if 'book' in cond:
            query = {'items': { '$exists': False }}
            query.update(self.unfinish)
            for unit in self.collect.find(query):
                result.append(unit['unit'])
            return result

        # units book(no finish)
        elif 'unfinish' in cond:
            for unit in self.collect.find(self.unfinish):
                result.append(unit['unit'])
            return result

        else:
            pass

    def find(self, cond):
        # cond form {'filter_key': unit}
        # all of this is unfinished

        if 'unit' in cond:
            query = {'unit': cond['unit']}
            query.update(self.unfinish)
            return self.collect.find_one(query)
        else:
            pass

    def server(self, msg):
        if 'op' in msg:
            handler = self.handle[msg['op']]
            del msg['op']
            handler(msg)
        else:
            pass

    def create(self, order):
        # for waiter
        order['time'] = { 'launch': time.time() }

        for i in range(len(order['items'])):
            query = {'tag': order['items'][i]['item']}
            order['items'][i]['item'] = self.cate.find(query)

        self.collect.insert(order)

    def read(self, order):
        # for casher
        query = {'unit':order['unit']}

        return self.find(query)

    def update(self, order):
        # for waitor
        query = {'unit':order['unit']}
        query.update(self.unfinish)

        for i in range(len(order['items'])):
            item = {'tag': order['items'][i]['item']}
            order['items'][i]['item'] = self.cate.find(item)

        modify = {'$addToSet': {'items': {'$each': orfer['items']}}}
        self.collect.update(query, modify)

    def delete(self, order):
        query = {'unit': order['unit']}
        query.update(self.unfinish)

        if 'items' in order:
            for item in order['items']:
                pull = {'$pull': {'items': item}}
                self.collect.update(query, pull)
        else:
            self.collect.remove(query)

    def checkout(self, order):
        # for casher
        query = {'unit':order['unit']}
        query.update(self.unfinish)

        unit = self.read(order)
        account = 0
        for item in unit['items']:
            account += self.cate.find({'cost':item['item']}) * item['amount']

        check = {'$set': {'account': account, 'time.finish': time.time()}}
        self.collect.update(query, check)


class User:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.collect = client.test.users

        self.key = [ "_id", "name", "passwd", "phone" ]

class Good:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.collect = client.test.goods

        self.key = [ "_id", "name", "price", "describe", "pic"]
