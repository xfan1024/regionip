#!/usr/bin/env python3
import sys
import netaddr

networks = []
for name in sys.argv[1:]:
    with open(name, 'r') as input_file:
        for line in input_file:
            networks.append(netaddr.IPNetwork(line))

for net in netaddr.cidr_merge(networks):
    print(str(net))
