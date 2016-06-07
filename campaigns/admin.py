from django.contrib import admin
from campaigns.models import Campaign
from users.models import meetia_user
from campaigns.models import Meeting
from campaigns.models import group_album
from campaigns.models import group_posts
from campaigns.models import group_posts_comments


admin.site.register(Campaign)
admin.site.register(meetia_user)
admin.site.register(Meeting)
admin.site.register(group_album)
admin.site.register(group_posts)
admin.site.register(group_posts_comments)


##  Register your models here.
