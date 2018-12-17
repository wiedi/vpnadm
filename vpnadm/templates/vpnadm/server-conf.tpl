mode server
proto {{ proto }}
port {{ port }}
dev tun0
persist-key
persist-tun

max-clients 2048
keepalive 10 60

topology subnet
client-to-client

verb 3
mute 20

status {{ openvpn_path }}/status 5
status-version 2
management {{ management_socket }} unix

## ciphers / tls
cipher AES-256-GCM
tls-version-min 1.2

tls-server
ca       {{ openvpn_path }}/certs/ca.crt
cert     {{ openvpn_path }}/certs/srv.crt
key      {{ openvpn_path }}/certs/srv.key
dh       {{ openvpn_path }}/certs/dh.pem
tls-auth {{ openvpn_path }}/certs/tls_auth.key 0

## client-connect/disconnect
script-security 3
client-connect "{{ manage_command }} client_connect"
#client-disconnect "{{ manage_command }} client_disconnect"
tmp-dir /tmp

## network settings
ifconfig      {{ server.server_ipv4 }} {{ server.ipv4_netmask }}
route-gateway {{ server.server_ipv4 }}
route {{ server.ipv4_default_net.network_address }} {{ server.ipv4_netmask }}

ifconfig-ipv6 {{ server.server_ipv6 }}/{{ server.ipv6_prefix }} {{ server.server_ipv6 }}
route-ipv6 {{ server.ipv6_default_net }}

## dynamic routes
{% for r in route4 %}
route {{ r }}{% endfor %}
{% for r in route6 %}
route-ipv6 {{ r }}{% endfor %}
