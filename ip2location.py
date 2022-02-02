#!/usr/bin/env python3
import sys
import netaddr
import requests
import json

def fetch_html(url):
    # with open('ip2location-china.html', 'r') as html_file:
    #     text = html_file.read()
    text = requests.get(url).text
    # with open('ip2location-china.html', 'w') as html_file:
    #     html_file.write(text)
    return text


def item_to_cidr(item):
    start = netaddr.IPAddress(item[0])
    end = netaddr.IPAddress(item[1])
    return netaddr.iprange_to_cidrs(start, end)

def main(args):
    xpath = '//*[@id="ip-address"]/tbody'
    url = 'http://assets-lite.ip2location.com/datasets/{}.json'.format(args[1])
    data_root = json.loads(fetch_html(url))
    data = data_root['data']
    for item in data:
        for net in item_to_cidr(item):
            print(str(net))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
