from django.utils import timezone
import datetime
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels




class Campaign(models.Model):
    group_name = models.CharField(max_length=30)
    group_members = models.IntegerField(
        default=1,
    )
    group_description = models.TextField(max_length=150)
    group_owner = models.ForeignKey(
        User,
        related_name="mgroups", #Meetia Groups
    )
    group_listofmembers = models.ManyToManyField(
        User,
        related_name="mberships" #Meetia Memberships
  , null=True , blank=True
    )
    group_image = models.ImageField(upload_to="group_images/" , null=True , blank=True)

    def __str__(self):
        return self.group_name

class Meeting(models.Model):
    meeting_name = models.CharField(max_length=30)
    meeting_description = models.TextField(max_length=150)
    meeting_date = models.DateField(default=datetime.datetime.now())
    meeting_group = models.ForeignKey(Campaign ,
                                      related_name="meeting_owner"
    )
    who_is_coming = models.ManyToManyField(User ,
                                           related_name='who_is_coming')
    meeting_location = models.TextField(max_length=50)
    def __str__(self):
        return self.meeting_name


class group_album(models.Model):
    group = models.ForeignKey(Campaign , related_name="album_group")
    pictures = models.ImageField(upload_to="group_images/")
    def __str__(self):
        return self.group.group_name


class group_posts(models.Model):
    posts = models.TextField()
    post_writer = models.ForeignKey(User , related_name="post_writer")
    post_title = models.TextField()
    group = models.ForeignKey(Campaign , related_name="group_posts")
    def __str__(self):
        return self.post_title

class group_posts_comments(models.Model):
    comments = models.TextField()
    comment_writer = models.ForeignKey(User , related_name="comment_writer")
    comment_for_post = models.ForeignKey(group_posts , related_name="comment_for_post")
    def __str__(self):
        return self.comment_for_post
