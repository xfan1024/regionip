#!/usr/bin/env python3
import sys
import netaddr
import requests
import json

def fetch(url):
    text = requests.get(url).text
    return text


def item_to_cidr(item):
    start = netaddr.IPAddress(item[0])
    end = netaddr.IPAddress(item[1])
    return netaddr.iprange_to_cidrs(start, end)

def main(args):
    url = 'http://cdn-lite.ip2location.com/datasets/{}.json'.format(args[1])

    data_root = json.loads(fetch(url))
    data = data_root['data']
    for item in data:
        for net in item_to_cidr(item):
            print(str(net))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
