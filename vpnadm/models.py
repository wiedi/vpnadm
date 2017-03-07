from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
import ipaddress
from vpnadm.utils import *
import itertools
import ipaddress




class Client(models.Model):
	user          = models.ForeignKey(User)
	name          = models.CharField(max_length=255)
	password      = models.CharField(max_length=255)
	ipv4          = models.GenericIPAddressField(protocol = 'IPv4', unique = True)
	ipv6          = models.GenericIPAddressField(protocol = 'IPv6', unique = True)

	def username(self):
		return self.user.username + '-' + slugify(self.name) + '-' + str(self.id)
	
	def set_password(self, password):
		self.password = make_password(password)


class ServerSettings(SingletonModel):
	first_ipv4  = models.GenericIPAddressField(protocol = 'IPv4', default='10.0.0.2')
	last_ipv4   = models.GenericIPAddressField(protocol = 'IPv4', default='10.0.0.253')

	first_ipv6  = models.GenericIPAddressField(protocol = 'IPv6', default='fd00:db8::3')
	last_ipv6   = models.GenericIPAddressField(protocol = 'IPv6', default='fd00:db8::ffff')

	def ipv4_nets(self):
		return ipaddress.summarize_address_range(
			ipaddress.ip_address(self.first_ipv4),
			ipaddress.ip_address(self.last_ipv4)
		)

	def ipv6_nets(self):
		return ipaddress.summarize_address_range(
			ipaddress.ip_address(self.first_ipv6),
			ipaddress.ip_address(self.last_ipv6)
		)

	def _allocate(self, nets, used_addresses):
		for addr in itertools.chain(*nets):
			if str(addr) not in used_addresses:
				return addr
		return None

	def allocate_v4(self):
		nets = self.ipv4_nets()
		used = list(Client.objects.values_list('ipv4', flat=True))
		return self._allocate(nets, used)

	def allocate_v6(self):
		nets = self.ipv6_nets()
		used = list(Client.objects.values_list('ipv6', flat=True))
		return self._allocate(nets, used)
	
