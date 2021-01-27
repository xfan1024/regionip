#!/bin/sh
set -e

dnsmasq_china_list_file_url=https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf


generate_dns_rule_head(){
echo '[outland]
server=${outland_dns}
*

[inland]
server=${mainland_dns}
${direct_list}'
}


generate_dns_rule(){
    echo write head to "$1" ... && generate_dns_rule_head >"$1"
    echo download data and write to "$1" ... && curl $dnsmasq_china_list_file_url | cut -d/ -f2 >> "$1"
    echo generate "$1".gz ... && gzip -fk "$1"
}

generate_ip_rule(){
    echo download data and write to "$1" ... && ./ip2location.py china >"$1"
    echo generate "$1".gz ... && gzip -fk "$1"
}

generate_dns_rule dns_rule
generate_ip_rule ip_rule
