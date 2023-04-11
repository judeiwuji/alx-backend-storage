#!/usr/bin/env python3
"""Log stats"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx

    print("{:d} logs".format(nginx.count_documents({})))
    print("Methods:")
    print("\tmethod GET: {:d}".format(
        nginx.count_documents({"method": "GET"})))
    print("\tmethod POST: {:d}".format(
        nginx.count_documents({"method": "POST"})))
    print("\tmethod PUT: {:d}".format(
        nginx.count_documents({"method": "PUT"})))
    print("\tmethod PATCH: {:d}".format(
        nginx.count_documents({"method": "PATCH"})))
    print("\tmethod DELETE: {:d}".format(
        nginx.count_documents({"method": "DELETE"})))
    print("{:d} status check".format(
        nginx.count_documents({"method": "GET", "path": "/status"})))
