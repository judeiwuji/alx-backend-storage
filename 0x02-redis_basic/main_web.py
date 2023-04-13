#!/usr/bin/env python3
"""
Main file
"""
get_page = __import__("web").get_page
redis = __import__("web").redis

if __name__ == "__main__":
    for _ in range(10):
        url = "http://plotterwave.com"
        get_page(url)
        print(redis.get("count:{}".format(url)))
