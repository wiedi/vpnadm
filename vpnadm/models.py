import ipaddress
import itertools
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth.hashers import make_password
from vpnadm.utils import *
from vpnadm.crypto import *


class Client(models.Model):
	user          = models.ForeignKey(User)
	name          = models.CharField(max_length = 255)
	ipv4          = models.GenericIPAddressField(protocol = 'IPv4', unique = True)
	ipv6          = models.GenericIPAddressField(protocol = 'IPv6', unique = True)

	key           = models.TextField(blank = True)
	crt           = models.TextField(blank = True)
	serial        = models.CharField(blank = True, max_length = 128)

	def cn(self):
		return self.user.username + '-' + slugify(self.name) + '-' + str(self.id)

	def __str__(self):
		return self.cn()

	def generate_keys(self):
		s = ServerSettings.get()
		self.serial = generate_serial()
		self.key    = generate_private_key_pem()
		self.crt    = sign_key(
			client_key_pem = self.key,
			ca_key_pem     = s.ca_key,
			ca_crt_pem     = s.ca_crt,
			cert_type      = 'CLIENT',
			cn             = self.cn(),
			serial         = self.serial
		)
		self.save()



class Route4(models.Model):
	target  = models.GenericIPAddressField(protocol = 'IPv4')
	netmask = models.GenericIPAddressField(protocol = 'IPv4')
	client  = models.ForeignKey(Client, null = True, blank = True)

	def __str__(self):
		return self.target + ' ' + str(self.netmask)


class Route6(models.Model):
	target  = models.GenericIPAddressField(protocol = 'IPv6')
	prefix  = models.IntegerField(default = 64)
	client  = models.ForeignKey(Client, null = True, blank = True)

	def __str__(self):
		return self.target + '/' + str(self.prefix)


class ServerSettings(SingletonModel):
	ca_key       = models.TextField(blank = True)
	ca_crt       = models.TextField(blank = True)
	ta_key       = models.TextField(blank = True)
	dh           = models.TextField(blank = True)

	first_ipv4   = models.GenericIPAddressField('First Client IPv4 Address', protocol = 'IPv4', default='10.0.0.2')
	last_ipv4    = models.GenericIPAddressField('Last Client IPv4 Address',  protocol = 'IPv4', default='10.0.0.253')
	ipv4_netmask = models.GenericIPAddressField('IPv4 Client Netmask',       protocol = 'IPv4', default='255.255.255.0')

	first_ipv6  = models.GenericIPAddressField('First Client IPv6 Address', protocol = 'IPv6', default='fd00:db8::3')
	last_ipv6   = models.GenericIPAddressField('Last Client IPv6 Address', protocol = 'IPv6', default='fd00:db8::ffff')
	ipv6_prefix = models.IntegerField('IPv6 Client Prefixlength', default = 64)

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
	
