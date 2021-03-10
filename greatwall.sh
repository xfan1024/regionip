#!/bin/bash

# some script boy alaways try to login to my server from abroad
# this scirpt can block these traffic to improve security and save bandwidth

set -e
#ip_rule=/root/ip_rule
ip_rule="$(dirname $0)/ip_rule"
set_name=greatwall
ipt_chain=greatwall

generate_ipset_restore_content()
{
	echo -N $set_name nethash
	awk '{print "add '$set_name' "$1}' <"$ip_rule"
}

_disable_greatwall()
{
	iptables -D INPUT -j $ipt_chain || true
	iptables -F $ipt_chain || true
	iptables -X $ipt_chain || true
	ipset destroy $set_name || true
}

disable_greatwall()
{
	_disable_greatwall >/dev/null
}

enable_greatwall()
{
	disable_greatwall
	generate_ipset_restore_content | ipset restore
	iptables-restore <<EOF
*filter
-N $ipt_chain
-A $ipt_chain -m set --match-set $set_name src -j ACCEPT
-A $ipt_chain -j DROP
-A INPUT -j $ipt_chain
COMMIT
EOF
}

case $1 in 
	enable)
		enable_greatwall
		;;
	disable)
		disable_greatwall
		;;
	*)
		echo "usage: $0 enable|disable"
		;;
esac

