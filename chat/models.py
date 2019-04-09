import calendar
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
	member = models.ManyToManyField(User)

	def __str__(self):
		return str(self.id)

	def all_members(self):
		return self.member.all()

	def all_messages(self):
		return Message.objects.filter(room = self)

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

	def date_time_format(self):
		return str(self.date.hour) + ':' + str(self.date.minute)

	def date_date_format(self):
		date = self.date
		return str(self.date.day) + 'th ' + calendar.month_name[self.date.month]

	# def message_pack(self):
	# 	images_pack = list()
	# 	images = self.image.all()
	# 	for image in images:
	# 		images_pack.append(image.image.url)
	# 	message_pack = {
	# 		'id': self.id,
	# 		'author':{'first_name':self.author.first_name, 'last_name':self.author.last_name, 'username': self.author.username, 'id': self.author.id},
	# 		'text': self.text,
	# 		'date': self.date_date_format(),
	# 		'time': self.date_time_format(),
	# 		'images': images_pack,
	# 		'not_read': True,
	# 		'need_update': True
	# 	}
	# 	return message_pack

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
			'date': self.date_date_format(),
			'time': self.date_time_format(),
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
