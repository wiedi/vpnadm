from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	args = ''
	help = 'generate a new CA'

	def handle(self, *args, **options):
		ca_crt, ca_key = generate_ca()

		s = ServerSettings.get()
		s.ca_crt = ca_crt.decode('utf-8')
		s.ca_key = ca_key.decode('utf-8')
		s.save()

		print(s.ca_crt)
		print(s.ca_key)