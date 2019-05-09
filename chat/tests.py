import unittest
import random
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User

class FirstTest(TestCase):
	def setUp(self):
		self.c = Client()

	def test_welcome_page(self):
		response = self.c.get('/')
		self.assertEqual(response.status_code, 200)

	def test_all_profiles(self):
		names = ['John', 'Will', 'Mary', 'Nickole', 'Larry', 'Alice', 'Sam', 'Ricky', 'Laura', 'Rita']
		lasts = ['Hayword', 'Larsson', 'Le Blanc', 'Conroy', 'Malony', 'Vega', 'Warner', 'Collins', 'Torrance']
		for i in range(5):
			name = random.choice(names)
			last = random.choice(lasts)
			username = name + '_' + last
			user = User.objects.create(username = username, first_name = name, last_name= last)
			user.set_password('12345678')
			user.save()
		all_users = User.objects.all()
		print(all_users)
		for user in all_users:
			url = '/profile/' + user.username
			response = self.c.get(url)
			self.assertEqual(response.status_code, 200)
