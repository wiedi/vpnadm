import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	args = ''
	help = 'generate a new DH parameter'

	def handle(self, *args, **options):
		dh = subprocess.check_output(['openssl', 'dhparam', '4096'], stderr = None).decode("utf-8").strip()
		s = ServerSettings.get()
		s.dh = dh
		s.save()

		print('Done')
