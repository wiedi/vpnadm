client
remote {{ server.hostname }}
verify-x509-name {{ server.hostname }} name
port {{ server.port }}
proto {{ server.proto }}
dev tun
topology subnet
auth-nocache
explicit-exit-notify
cipher AES-256-GCM
tls-version-min 1.2
remote-cert-tls server

# default route choices:
# nothing - no default route
# ipv4 only:
#	route-gateway {{ server.server_ipv4 }}
#	redirect-gateway def1
# ipv6 only:
#	redirect-gateway ipv6 !ipv4
# ipv4 + ipv6:
#	route-gateway {{ server.server_ipv4 }}
#	redirect-gateway ipv6 def1

<ca>
{{ server.ca_crt }}</ca>
<cert>
{{ client.crt }}</cert>
<key>
{{ client.key }}</key>
key-direction 1
<tls-auth>
{{ server.ta_key }}</tls-auth>
