import unittest
import random
from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from faker import Faker
from chat.models import Room, Message


import pytest
from channels.testing import WebsocketCommunicator
from chat.consumers import CommonRoomConsumer


class ComplicatedSeleniumTests(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.browsers_number = random.randint(2, 20)
		cls.selenium_list = list()
		for i in range(cls.browsers_number):
			cls.selenium_list.append( WebDriver())
			cls.selenium_list[i].implicitly_wait(10)

	@classmethod
	def tearDownClass(cls):
		for i in range(cls.browsers_number):
			cls.selenium_list[i].quit()
		super().tearDownClass()

	def create_users(self, counter):
		factory = Faker()
		users_list = list()
		for i in range(counter):
			username = 'username' + str(i)
			password = factory.password()
			first_name = factory.first_name()
			last_name = factory.first_name()
			user = User.objects.create(username = username, first_name = first_name, last_name= last_name)
			user.set_password(password)
			user.save()
			users_list.append({'username': username, 'password': password})
		return users_list

	def test_simple_chatting(self):
		chatters = self.create_users(self.browsers_number)
		room = Room.objects.create()
		factory = Faker()
		for chatter in chatters:
			user = User.objects.get(username = chatter['username'])
			room.member.add(user)
		for i in range(self.browsers_number):
			self.selenium_list[i].get('%s%s' % (self.live_server_url, '/'))
			username_input = self.selenium_list[i].find_element_by_name("username")
			username_input.send_keys(chatters[i]['username'])
			password_input = self.selenium_list[i].find_element_by_name("password")
			password_input.send_keys(chatters[i]['password'])
			self.selenium_list[i].find_element_by_id('login_button').click()
			room_url = '/chat/room/' + str(room.id)
			self.selenium_list[i].get('%s%s' % (self.live_server_url, room_url))


class SimpleSeleniumTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def create_user_exemplar(self, counter):
    	factory = Faker()
    	users_list = list()
    	for i in range(counter):
    		username = 'username' + str(i)
    		password = factory.password()
    		first_name = factory.first_name()
    		last_name = factory.first_name()
    		user = User.objects.create(username = username, first_name = first_name, last_name= last_name)
    		user.set_password(password)
    		user.save()
    		users_list.append({'username': username, 'password': password})
    	return users_list


    def test_login(self):
	    user = self.create_user_exemplar(1)[0]
	    self.selenium.get('%s%s' % (self.live_server_url, '/'))
	    username_input = self.selenium.find_element_by_name("username")
	    username_input.send_keys(user['user']['username'])
	    password_input = self.selenium.find_element_by_name("password")
	    password_input.send_keys(user['password'])
	    self.selenium.find_element_by_id('login_button').click()
	    logout = self.selenium.find_element_by_id('logout')


    def test_registration(self):
    	self.selenium.get('%s%s' % (self.live_server_url, '/registration'))
    	username_input = self.selenium.find_element_by_name("username")
    	username_input.send_keys('NewRegistratedUser')
    	first_name_input = self.selenium.find_element_by_name("first_name")
    	first_name_input.send_keys("FirstName")
    	last_name_input = self.selenium.find_element_by_name("last_name")
    	last_name_input.send_keys("LastName")
    	email_input = self.selenium.find_element_by_name("email")
    	email_input.send_keys("test@mail.com")
    	password_input = self.selenium.find_element_by_name("password1")
    	password_input.send_keys("12345678")
    	confirm_input = self.selenium.find_element_by_name("password2")
    	confirm_input.send_keys("12345678")
    	self.selenium.find_element_by_xpath('//input[@value="Register"]').click()
    	self.selenium.find_element_by_id('logout'):
