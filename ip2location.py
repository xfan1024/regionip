#!/usr/bin/env python3
import sys
import netaddr
import requests
from lxml import etree

def fetch_html(url):
    # with open('ip2location-china.html', 'r') as html_file:
    #     text = html_file.read()
    text = requests.get(url).text
    # with open('ip2location-china.html', 'w') as html_file:
    #     html_file.write(text)
    return text


def tr_to_cidr(tr):
    _, td_start, _, td_end, _, td_size, _ = tr.getchildren()
    start = netaddr.IPAddress(td_start.text)
    end = netaddr.IPAddress(td_end.text)
    size = int(td_size.text.replace(',', ''))
    assert(end.value - start.value + 1 == size)
    return netaddr.iprange_to_cidrs(start, end)
    
    

def main(args):
    xpath = '//*[@id="ip-address"]/tbody'
    url = 'https://lite.ip2location.com/{}-ip-address-ranges'.format(args[1])
    html = etree.HTML(fetch_html(url))
    for tr in html.xpath(xpath)[0]:
        for net in tr_to_cidr(tr):
            print(str(net))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
