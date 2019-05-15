import calendar
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class ChatProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to="avatar_images/", null = True, blank = True)
	birthday = models.DateField(null=True, blank=True)
	city = models.CharField(null=True, blank=True, max_length=100)

	def __str__(self):
		return self.user.username

	def avatar_url(self):
		if self.avatar:
			return self.avatar.url
		else:
			return '/static/service/avatar.jpg'

	def user_dict(self):
		user_dict = {'id': self.user.id, 'first_name': self.user.first_name, 'last_name': self.user.last_name, 'avatar': self.avatar_url()}
		return user_dict

	def formated_birth_day(self):
		# return self.birthday
		# print(type(self.birthday))
		# print(self.birthday.year)
		# print(self.birthday.day)
		# print(self.birthday.month)
		return calendar.month_name[self.birthday.month] + ' ' + str(self.birthday.day) + ', ' + str(self.birthday.year)

class Room(models.Model):
	member = models.ManyToManyField(User)

	def __str__(self):
		return str(self.id)

	def all_members(self):
		return self.member.all()

	def all_members_list(self):
		ms = self.all_members()
		ms_list = list()
		for m in ms:
			m_dict = {
				'first_name': m.first_name,
				'last_name': m.last_name
			}
			ms_list.append(m_dict)
		return ms_list

	def all_messages(self):
		return Message.objects.filter(room = self)

	def last_message_title(self, user):
		last_message = Message.objects.filter(room = self).first()
		if last_message != None:
			return last_message.title_message_pack(user)
		else:
			return False

	def title_name(self):
		title_name = ''
		members = self.all_members()
		if len(members)>3:
			for index in range(3):
				m = members[index]
				title_name = title_name + m.first_name + ' ' + m.last_name
				if (index != len(members)-1):
					title_name = title_name + ', '
				else:
					title_name = title_name + '...'
		else:
			for index in range(len(members)):
				m = members[index]
				title_name = title_name + m.first_name + ' ' + m.last_name		
				if (index != len(members)-1):
					title_name = title_name + ', '
		return title_name


class Message(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
	text = models.CharField(max_length=200, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	had_read = models.ManyToManyField(User)
	image = models.ManyToManyField('MessageImage', blank=True)

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return self.author.username + ' at ' + str(self.date)

	def title_message_pack(self, user):
		if self.author == user:
			mine = True
		else:
			mine = False
		if self.text:
			splitted_text = self.text.split(' ')
			if len(splitted_text)<4:
				title_text = self.text
			else:
				title_text = ' '.join(splitted_text[:3]) + '...'
		else:
			title_text = False
		title_dict = {
			'id': self.id,
			'author':{'first_name':self.author.first_name, 
					  'last_name':self.author.last_name, 
					  'username': self.author.username, 
					  'id': self.author.id,
					  'avatar': self.author.chatprofile.avatar_url()},
			'title_text': title_text,
			'img_amount': len(self.image.all()),
			'date': self.final_date_format(),
			'not_read': self.green_message_for_user(user),
			'need_update': self.need_read_and_update(user),
			'mine': mine
		}	
		return title_dict	

	def final_date_format(self):
		one_day = timedelta(days = 1)
		now = timezone.now()
		if self.date < now - one_day:
			return self.date_date_format()
		else:
			return self.date_time_format()
 
	def date_time_format(self):
		return str(self.date.hour) + ':' + str(self.date.minute)

	def date_date_format(self):
		date = self.date
		return str(self.date.day) + 'th ' + calendar.month_name[self.date.month]

	def packed_dict(self, user):
		images_pack = list()
		images = self.image.all()
		for image in images:
			images_pack.append(image.image.url)
		if self.author == user:
			mine = True
		else:
			mine = False
		packed_dict = {
			'id': self.id,
			'author':{'first_name':self.author.first_name, 'last_name':self.author.last_name, 'username': self.author.username, 'id': self.author.id},
			'text': self.text,
			'date': self.final_date_format(),
			'images': images_pack,
			'not_read': self.green_message_for_user(user),
			'need_update': self.need_read_and_update(user),
			'mine': mine
		}
		return packed_dict		

	def has_not_user_read(self, user):
		if user in self.had_read.all():
			return False
		else:
			return True

	def green_message_for_user(self, user):
		if user == self.author:
			if self.had_read.all().count() < 2:
				return True
			else:
				return False
		else:
			return self.has_not_user_read(user)	

	def white_message_for_user(self, user):
		if user == self.author:
			if self.had_read.all().count() < 2:
				return False
			else:
				return True
		else:
			if self.has_not_user_read(user):
				return False
			else:
				return True		

	def need_read_and_update(self, user):
		if user != self.author:
			if self.green_message_for_user(user):
				return True
			else:
				return False
		else:
			return False

class MessageImage(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="message_images/", null = True, blank = True)

	def __str__(self):
		return self.image.url
