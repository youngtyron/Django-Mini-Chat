import unittest
import random
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

# class FirstTest(TestCase):
# 	def setUp(self):
# 		self.c = Client()

# 	def test_welcome_page(self):
# 		response = self.c.get('/')
# 		self.assertEqual(response.status_code, 200)

# 	def test_all_profiles(self):
# 		names = ['John', 'Will', 'Mary', 'Nickole', 'Larry', 'Alice', 'Sam', 'Ricky', 'Laura', 'Rita']
# 		lasts = ['Hayword', 'Larsson', 'Le Blanc', 'Conroy', 'Malony', 'Vega', 'Warner', 'Collins', 'Torrance']
# 		for i in range(5):
# 			name = random.choice(names)
# 			last = random.choice(lasts)
# 			username = name + '_' + last
# 			user = User.objects.create(username = username, first_name = name, last_name= last)
# 			user.set_password('12345678')
# 			user.save()
# 		all_users = User.objects.all()
# 		print(all_users)
# 		for user in all_users:
# 			url = '/profile/' + user.username
# 			response = self.c.get(url)
# 			self.assertEqual(response.status_code, 200)


class MySeleniumTests(StaticLiveServerTestCase):
    # fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def create_user_exemplar(self):
    	user = User.objects.create(username = 'NewUser', first_name = 'Test', last_name= 'User')
    	user.set_password('12345678')
    	user.save()    	

    def test_login(self):
    	self.create_user_exemplar()
    	self.selenium.get('%s%s' % (self.live_server_url, '/'))
    	username_input = self.selenium.find_element_by_name("username")
    	username_input.send_keys('NewUser')
    	password_input = self.selenium.find_element_by_name("password")
    	password_input.send_keys('12345678')
    	self.selenium.find_element_by_id('login_button').click()
    	logout = self.selenium.find_element_by_id('logout')
