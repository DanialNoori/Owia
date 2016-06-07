from django.db import models
from django.contrib.auth.models import User
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class meetia_user(models.Model):
    profile_picture = models.ImageField(upload_to="user_images/" , null=True , blank= True)
    user = models.OneToOneField(
        User,
    )
    def __str__(self):
        return self.user.username


class message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(User , related_name="messae_sender")
    receiver = models.ForeignKey(User , related_name="message_receiver")

# Create your models here.

class PasswordToken(models.Model):
    user = models.ForeignKey(
        User,
        unique=True
    )
    token = models.CharField(
        max_length=20
    )

    def __str__(self):
        return "Token: " + self.token.__str__() + " for " + self.user.username