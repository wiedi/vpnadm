import os
import sys
from django.utils.timezone import now
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	help = 'call-back script for openvpn client-disconnect event'

	def handle(self, *args, **options):
		try:
			cn     = os.environ['common_name']

			pk = int(cn.split('-')[-1])
			c = Client.objects.get(pk = pk)

			if c.cn() != cn:
				raise Exception("CN does not match")

			c.last_connection_change = now()
			c.connected              = False
			c.bytes_received        += int(os.environ['bytes_received'])
			c.bytes_sent            += int(os.environ['bytes_sent'])
			c.connected_duration    += int(os.environ['time_duration'])
			c.save()

			return
		except Exception as e:
			print(e)
			sys.exit(1)