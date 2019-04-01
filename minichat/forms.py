from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=16,
							  min_length = 2,
							  required=True,
							  label='Username',
							  widget = forms.TextInput(attrs = {'class':'form-control'}))
	first_name = forms.CharField(max_length=20,
								min_length = 2,
								required=True,
								label='First name',
								widget = forms.TextInput(attrs = {'class':'form-control'}))
	last_name = forms.CharField(max_length=20,
								min_length = 2,
								required=True,
								label='Last name',
								widget = forms.TextInput(attrs = {'class':'form-control'}))
	email = forms.EmailField(required=True,
							 label='Email',
							 widget=forms.TextInput(attrs = {'class':'form-control'}))
	password = forms.CharField(label = 'Password',
							   max_length = 30,
	                		   min_length = 6,
	                		   required=True,
	                		   widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	confirm = forms.CharField(label = 'Confirm password',
                    		  max_length = 30,
                      		  min_length = 6,
                      		  required=True,
                    		  widget = forms.PasswordInput(attrs = {'class':'form-control'}))

	def clean_email(self):
		email = self.cleaned_data['email']
		existing_user = User.objects.filter(email = email)
		if existing_user.exists():
			raise ValidationError('This email adress is already used')
		return email

	def clean_password(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		confirm = cleaned_data.get('confirm')
		if password and confirm:
			if password != confirm:
				raise ValidationError('Invalid password')
