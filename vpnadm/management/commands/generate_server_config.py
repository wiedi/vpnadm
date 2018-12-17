import sys
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.loader import render_to_string
from vpnadm.crypto import *
from vpnadm.models import *


class Command(BaseCommand):
	args = ''
	help = 'generate openvpn server config'

	def handle(self, *args, **options):
		print(render_to_string('vpnadm/server-conf.tpl', {
			'openvpn_path':      settings.OPENVPN_PATH,
			'proto':             settings.OPENVPN_PROTO,
			'port':              settings.OPENVPN_SERVER_PORT,
			'management_socket': settings.OPENVPN_MANAGEMENT_SOCKET,
			'manage_command':    settings.MANAGE_COMMAND,
			'server':            ServerSettings.get(),
			'route4':            Route4.objects.all(),
			'route6':            Route6.objects.all(),
		}))
