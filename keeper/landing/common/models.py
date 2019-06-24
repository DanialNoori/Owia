from django.db import models

# Create your models here.
class Subscriber(models.Model):
	email_address = models.CharField(max_length=200)
	activated = models.BooleanField(default=False)

	def __str__(self):
		return self.email_address