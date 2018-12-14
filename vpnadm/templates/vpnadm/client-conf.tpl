client
remote {{ server.hostname }}
port {{ server.port }}
proto {{ server.proto }}
dev tun
tun-ipv6
auth-user-pass
auth-nocache
cipher AES-256-CBC
tls-cipher TLS-DHE-RSA-WITH-AES-256-GCM-SHA384
auth SHA512
tls-version-min 1.2
remote-cert-tls server
<ca>
{{ server.ca_crt }}</ca>
<cert>
{{ client.crt }}</cert>
<key>
{{ client.key }}</key>
key-direction 1