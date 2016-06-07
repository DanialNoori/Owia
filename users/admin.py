from django.contrib import admin
from users.models import message, PasswordToken

admin.site.register(message)
admin.site.register(PasswordToken)
