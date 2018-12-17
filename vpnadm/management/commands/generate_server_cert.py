from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	help = 'generate a new server certificate'

	def add_arguments(self, parser):
		parser.add_argument('key_file',  type=str, help='Path to the key file (PEM)')
		parser.add_argument('cert_file', type=str, help='Path to the cert file (PEM)')

	def handle(self, *args, **options):
		key_file  = options['key_file']
		cert_file = options['cert_file']

		s = ServerSettings.get()
		key = generate_private_key_pem()
		crt = sign_key(
			client_key_pem = key,
			ca_key_pem     = s.ca_key,
			ca_crt_pem     = s.ca_crt,
			cert_type      = 'SERVER',
			cn             = settings.OPENVPN_HOSTNAME,
			serial         = generate_serial()
		)

		open(key_file, 'wb').write(key.encode('utf-8'))
		open(cert_file, 'wb').write(crt.encode('utf-8'))
