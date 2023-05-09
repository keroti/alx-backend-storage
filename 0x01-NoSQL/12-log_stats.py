#!/usr/bin/env python3
'''
Function that provides some stats about Nginx logs stored in MongoDB
'''

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
database = client.logs
nginx_collection = database.nginx

# Number of documents in collection
num_logs = nginx_collection.count_documents({})
print(f"{num_logs} logs")

# Number of documents with each method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    num_docs = nginx_collection.count_documents({"method": method})
    print(f"    method {method}: {num_docs}")

# Number of documents with method GET and path /status
num_status_check = nginx_collection.count_documents(
    {"method": "GET", "path": "/status"}
    )
print(f"{num_status_check} status check")

if __name__ == '__main__':
    run()
