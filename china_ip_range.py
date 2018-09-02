#!/usr/bin/env python
from __future__ import print_function
import urllib2
import re
import sys

if len(sys.argv) >= 2 and sys.argv[1] == '--stdin':
    use_stdin = True
else:
    use_stdin = False

from math import log

if use_stdin:
    origin = sys.stdin
else:
    origin = urllib2.urlopen('http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest')

cnipv4_pattern = re.compile('^[^\|]+\|CN\|ipv4\|([^\|]+)\|([^\|]+)\|[^\|]+\|[^\|]+$')


for line in origin:
    match = cnipv4_pattern.match(line)
    if match:
        ip_start = match.group(1)
        size = int(match.group(2))
        cidr = 32 - (log(size) / log(2))
        assert(cidr.is_integer())
        # print('# ' + line.strip())
        print('%s/%d' % (ip_start, int(cidr)))


