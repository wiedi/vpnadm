from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	args = ''
	help = 'generate a new CA'

	def handle(self, *args, **options):
		ca_crt, ca_key = generate_ca(
			lifetime            = settings.CA_LIFETIME_IN_DAYS,
		)

		s = ServerSettings.get()
		s.ca_crt = ca_crt
		s.ca_key = ca_key
		s.save()

		print('Done')