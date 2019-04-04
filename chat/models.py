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

	def message_pack(self):
		images_pack = list()
		images = self.image.all()
		for image in images:
			images_pack.append(image.image.url)
		message_pack = {
			'author':{'first_name':self.author.first_name, 'last_name':self.author.last_name, 'username': self.author.username},
			'text': self.text,
			'date': self.date_date_format(),
			'time': self.date_time_format(),
			'images': images_pack
		}
		return message_pack

class MessageImage(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="message_images/", null = True, blank = True)

	def __str__(self):
		return self.image.url
