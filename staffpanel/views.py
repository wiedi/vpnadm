from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import Context, Template
from django.conf import settings
from braces import views

from staffpanel.forms import UserCreateForm

class UserList(LoginRequiredMixin, views.StaffuserRequiredMixin, ListView):
	model = User


class UserDelete(LoginRequiredMixin, views.StaffuserRequiredMixin, DeleteView):
	model = User
	success_url = reverse_lazy('staffpanel_user_list')


@staff_member_required
def user_create(request):
	form = UserCreateForm(request.POST or None)
	if form.is_valid():
		
		u = User(
			username = form.cleaned_data['username'],
			email    = form.cleaned_data['email'],
		)
	
		new_password = User.objects.make_random_password(length=20)
		u.set_password(new_password)
		
		u.save()

		messages.info(request, 'Password for "{user}" set to "{password}".'.format(
			user     = u.username,
			password = new_password
		))
		return redirect('staffpanel_user_list')
	return render(request, 'auth/user_form.html', {'form': form})



@require_POST
@staff_member_required
def user_reset_password(request, pk):
	u = get_object_or_404(User, pk = pk)
	new_password = User.objects.make_random_password(length=20)
	u.set_password(new_password)
	u.save()

	messages.info(request, 'Password for "{user}" set to "{password}".'.format(
		user     = u.username,
		password = new_password
	))

	return redirect('staffpanel_user_list')


@require_POST
@staff_member_required
def user_disable(request, pk):
	u = get_object_or_404(User, pk = pk)
	u.is_active = False
	u.save()
	return redirect('staffpanel_user_list')

@require_POST
@staff_member_required
def user_enable(request, pk):
	u = get_object_or_404(User, pk = pk)
	u.is_active = True
	u.save()
	return redirect('staffpanel_user_list')


@require_POST
@staff_member_required
def user_set_staff(request, pk):
	u = get_object_or_404(User, pk = pk)
	u.is_staff = True
	u.save()
	return redirect('staffpanel_user_list')

@require_POST
@staff_member_required
def user_unset_staff(request, pk):
	u = get_object_or_404(User, pk = pk)
	u.is_staff = False
	u.save()
	return redirect('staffpanel_user_list')
