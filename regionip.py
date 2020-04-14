#!/usr/bin/env python3
import sys
import argparse
import re
import netaddr
from os import path

def update():
    print('update no implementation', file=sys.stderr)
    return 1

def write_ip_range(o, ipstart, ipstop):
    for net in netaddr.iprange_to_cidrs(ipstart, ipstop - 1):
        print(str(net), file = o)

def main(args):
    prog = args[0]
    source_path = path.dirname(prog)
    origin_data_path = path.join(source_path, 'apnic-latest.txt')
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', action='store_true', default=False)
    parser.add_argument('--exclude', action='store_true', default=False)
    parser.add_argument('--allow-discontinuity', action='store', type=int, default=0)
    parser.add_argument('--allocated-only', action='store_true', default=False)
    parser.add_argument('--assigned-only', action='store_true', default=False)
    opt, region_code_list = parser.parse_known_args(args[1:])

    if opt.update:
        return update(origin_data_path)

    if len(region_code_list) == 0:
        print('region code least one is required', file=sys.stderr)
        return 1

    if not path.exists(origin_data_path):
        print('warning: origin-data not found, update now', file=sys.stderr)
        res = update(origin_data_path)
        if res != 0:
            return res

    region_code_list = set(region_code_list)
    code_pattern = re.compile("^[A-Z]+$")
    for code in region_code_list:
        if not code_pattern.match(code):
            print('incorrect region code: ' + code, file=sys.stderr)
            return 1

    if opt.allocated_only and opt.assigned_only:
        print('--allocated-only and --assigned-only can not be set both', file=sys.stderr)
        return 1

    require_type = None
    if opt.allocated_only:
        require_type = 'allocated'
    if opt.assigned_only:
        require_type = 'assigned'
    ipv4_pattern = re.compile('apnic\|([A-Z]+)\|ipv4\|([\d\.]+)\|(\d+)\|(\S+?)\|(\S+)')
    # group 1: region code
    # group 2: ipv4
    # group 3: amount
    # group 4: date
    # group 5: type
    prev_ipstart = None
    prev_ipstop = None
    with open(origin_data_path, 'r') as input_stream:
        for line in input_stream:
            m = ipv4_pattern.match(line)
            if not m:
                continue
            code, ipv4, amount, date, record_type = m.groups()
            if require_type is not None and require_type != record_type:
                # print('require: {}  record: {}'.format(require_type, record_type))
                continue

            in_code_list = code in region_code_list
            if opt.exclude and in_code_list:
                continue

            if not opt.exclude and not in_code_list:
                continue

            ipstart = netaddr.IPAddress(ipv4)
            ipstop = ipstart + int(amount)
            if prev_ipstart is None:
                prev_ipstart = ipstart
                prev_ipstop = ipstop
                continue

            assert(ipstart >= prev_ipstop)
            if ipstart.value - prev_ipstop.value <= opt.allow_discontinuity:
                prev_ipstop = ipstop
            else:
                write_ip_range(sys.stdout, prev_ipstart, prev_ipstop)
                prev_ipstart = ipstart
                prev_ipstop = ipstop
        if prev_ipstart is not None:
            write_ip_range(sys.stdout, prev_ipstart, prev_ipstop)

if __name__ == '__main__':
    main(sys.argv)
