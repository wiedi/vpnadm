from django import forms

class UserCreateForm(forms.Form):
	username    = forms.CharField()
	email       = forms.EmailField()
