#!/bin/sh
set -e

dnsmasq_china_list_base=https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master
dnsmasq_china_list_files='accelerated-domains.china.conf apple.china.conf google.china.conf'

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
    for file in $dnsmasq_china_list_files
    do
        url=$dnsmasq_china_list_base/$file
        echo download "$file" and write to "$1" ... && curl "$url" | cut -d/ -f2 >> "$1"
    done
    echo generate "$1".gz ... && gzip -fk "$1"
}

generate_ip_rule_apnic(){
    echo update apnic-latest.txt ... && ./regionip.py --update
    echo write to "$1" ... && ./regionip.py CN >"$1"
}

generate_ip_rule_ip2location(){
    echo download data and write to "$1" ... && ./ip2location.py china >"$1"
}

generate_ip_rule(){
    output="$1"
    shift
    echo generate "$output" ... && ./cidr_merge.py "$@" >"$output"
    echo generate "$output".gz ... && gzip -fk "$output"
}

generate_dns_rule dns_rule
generate_ip_rule_apnic ip_rule.apnic
generate_ip_rule_ip2location ip_rule.ip2location
generate_ip_rule ip_rule ip_rule.apnic ip_rule.ip2location
