#!/usr/bin/env python3
import sys
import netaddr
import requests
from lxml import etree

def fetch_html(url):
    # with open('ip2location-china.html', 'r') as html_file:
    #     return html_file.read()
    return requests.get(url).text


def tr_to_cidr(tr):
    td_start, td_end, td_size = tr.getchildren()
    start = netaddr.IPAddress(td_start.text)
    end = netaddr.IPAddress(td_end.text)
    size = int(td_size.text.replace(',', ''))
    assert(end.value - start.value + 1 == size)
    return netaddr.iprange_to_cidrs(start, end)
    
    

def main(args):
    xpath = '/html/body/div[2]/div/div/div/div/div/div/table/tbody'
    url = 'https://lite.ip2location.com/{}-ip-address-ranges'.format(args[1])
    html = etree.HTML(fetch_html(url))
    for tr in html.xpath(xpath)[0]:
        for net in tr_to_cidr(tr):
            print(str(net))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
