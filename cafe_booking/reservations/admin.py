from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Cafe,CustomUser

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Cafe)