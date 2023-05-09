#!/usr/bin/env python3
'''
Function that provides some stats about Nginx logs stored in MongoDB
'''
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    '''return number of documents in collection
    '''
    print('{} logs'.format(nginx_collection.count_documents({})))

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        num = len(list(nginx_collection.find({'method': method})))
        print(f"    method {method}: {num}")
    status_checks_num = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print(f"{status_checks_num} status check")


def run():
    '''Provides some stats about Nginx logs stored in MongoDB
    '''
    client = MongoClient('mongodb://localhost:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
