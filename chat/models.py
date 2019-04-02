from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
	member = models.ManyToManyField(User)

	def __str__(self):
		return str(self.id)

class Message(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
	room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
	text = models.CharField(max_length=200, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	had_read = models.ManyToManyField(User)
	image = models.ManyToManyField('MessageImage')

	def __str__(self):
		return self.author.username + ' at ' + str(self.date)

class MessageImage(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	image = models.ImageField(upload_to="message_images/", null = True, blank = True)
		
	def __str__(self):
		return self.image.url