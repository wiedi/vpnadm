import os
import sys
from django.utils.timezone import now
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	help = 'call-back script for openvpn client-connect event'

	def add_arguments(self, parser):
		parser.add_argument('tmpfile',  type=str, help='Path to tmpfile for per-client server config')

	def handle(self, *args, **options):
		try:
			cn     = os.environ['common_name']
			serial = os.environ['tls_serial_0']

			pk = int(cn.split('-')[-1])
			c = Client.objects.get(pk = pk)

			if c.cn() != cn:
				raise Exception("CN does not match")

			if serial != c.serial:
				raise Exception("Serial does not match. Possibly revoked cert")

			s = ServerSettings.get()
			client_conf = [
				"ifconfig-push "      + c.ipv4 + " " + s.ipv4_netmask,
				"ifconfig-ipv6-push " + c.ipv6 + "/" + str(s.ipv6_prefix),
			]

			for r4 in Route4.objects.all():
				client_conf += ['push "route ' + r4.client_route() + '"']

			for r6 in Route6.objects.all():
				client_conf += ['push "route-ipv6 ' + r6.client_route() + '"']

			for r4 in Route4.objects.filter(client = c):
				client_conf += ["iroute " + str(r4)]

			for r6 in Route6.objects.filter(client = c):
				client_conf += ["iroute-ipv6 " + str(r6)]

			client_conf += [""]
			open(options['tmpfile'], 'wb').write("\n".join(client_conf).encode('utf-8'))

			c.last_connection_change = now()
			c.connected      = True
			c.last_remote_ip = os.environ['trusted_ip']
			c.client_os      = os.environ['IV_PLAT']
			c.save()

			return
		except Exception as e:
			print(e)
			sys.exit(1)