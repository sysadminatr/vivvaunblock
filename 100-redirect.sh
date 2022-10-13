#!/bin/sh

[ "$type" == "ip6tables" ] && exit 0

if [ -z "$(iptables-save 2>/dev/null | grep unblock)" ]; then
    ipset create unblock hash:net -exist
    iptables -w -t nat -A PREROUTING -i br0 -p tcp -m set --match-set unblock dst -j REDIRECT --to-port 9141
    iptables -w -t nat -A PREROUTING -i ppp0 -p tcp -m set --match-set unblock dst -j REDIRECT --to-port 9141
    iptables -w -t nat -A PREROUTING -i l2tp0 -p tcp -m set --match-set unblock dst -j REDIRECT --to-port 9141
fi

exit 0
