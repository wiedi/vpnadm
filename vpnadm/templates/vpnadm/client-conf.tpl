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
<ca>
{{ server.ca_crt }}</ca>
<cert>
{{ client.crt }}</cert>
<key>
{{ client.key }}</key>
key-direction 1
<tls-auth>
{{ server.ta_key }}</tls-auth>
