import subprocess
import tempfile
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	args = ''
	help = 'generate a new tls-auth key'

	def handle(self, *args, **options):
		with tempfile.NamedTemporaryFile() as t:
			subprocess.check_output(['openvpn', '--genkey', '--secret', t.name])

			s = ServerSettings.get()
			s.ta_key = t.read().decode('utf-8')
			s.save()

		print(s.ta_key)
