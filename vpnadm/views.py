from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from vpnadm.models import *
from vpnadm.utils import *

@login_required
def status(request):
	return render(request, 'vpnadm/status.html', {'info': None})


class ClientList(LoginRequiredMixin, ListView):
	model = Client

	def get_queryset(self):
		if not self.request.user.is_staff:
			return Client.objects.filter(user = self.request.user)
		return Client.objects.all()


class ClientCreate(LoginRequiredMixin, CreateView):
	model = Client
	fields = ['name']
	success_url = reverse_lazy('client_list')

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user

		self.object.ipv4 = str(ServerSettings.get().allocate_v4() or '')
		self.object.ipv6 = str(ServerSettings.get().allocate_v6() or '')

		if not self.object.ipv4 or not self.object.ipv6:
			messages.error(self.request, "Failed to allocate IP Address")
			return redirect(self.success_url)

		self.object.save() # need PK for next step
		self.object.generate_keys()
		self.object.save()

		return super(ClientCreate, self).form_valid(form)


@require_POST
@login_required
def client_reset_cert(request, pk):
	c = get_object_or_404(Client, pk = pk)
	
	if not request.user.is_staff and c.user != request.user:
		raise Http404
	
	c.generate_keys()
	c.save()

	messages.success(request, "Key regenerated, please download your new config.")

	return redirect('client_list')

@login_required
def client_download_config(request, pk):
	c = get_object_or_404(Client, pk = pk)

	if not request.user.is_staff and c.user != request.user:
		raise Http404

	s = ServerSettings.get()
	conf = render_to_string('vpnadm/client-conf.tpl', {
		'client': c,
		'server': {
			'ca_crt':   s.ca_crt,
			'ta_key':   s.ta_key,
			'proto':    settings.OPENVPN_PROTO,
			'port':     settings.OPENVPN_SERVER_PORT,
			'hostname': settings.OPENVPN_HOSTNAME,
		},
	})
	response = HttpResponse(conf, content_type='application/octet-stream')
	response['Content-Disposition'] = 'attachment; filename="' + c.cn() + '.ovpn"'
	return response



class ClientDelete(LoginRequiredMixin, DeleteView):
	model = Client
	success_url = reverse_lazy('client_list')



class ServerSettingsUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = ServerSettings
	fields = [
		'server_ipv4',
		'first_ipv4',
		'last_ipv4',
		'ipv4_netmask',
		'server_ipv6',
		'first_ipv6',
		'last_ipv6',
		'ipv6_prefix',
	]
	success_url = reverse_lazy('serversettings_update')
	success_message = "Settings saved"

	def get_object(self, queryset = None):
		return ServerSettings.get()


class Route4List(StaffRequiredMixin, ListView):
	model = Route4

	def get_queryset(self):
		if not self.request.user.is_staff:
			return Route4.objects.none()
		return Route4.objects.all()

class Route4Create(StaffRequiredMixin, CreateView):
	model = Route4
	fields = ['target', 'netmask', 'client']
	success_url = reverse_lazy('route4_list')

class Route4Delete(StaffRequiredMixin, DeleteView):
	model = Route4
	success_url = reverse_lazy('route4_list')


class Route6List(StaffRequiredMixin, ListView):
	model = Route6

	def get_queryset(self):
		if not self.request.user.is_staff:
			return Route6.objects.none()
		return Route6.objects.all()

class Route6Create(StaffRequiredMixin, CreateView):
	model = Route6
	fields = ['target', 'prefix', 'client']
	success_url = reverse_lazy('route6_list')

class Route6Delete(StaffRequiredMixin, DeleteView):
	model = Route6
	success_url = reverse_lazy('route6_list')
