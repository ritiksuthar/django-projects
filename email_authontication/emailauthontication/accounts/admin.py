from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile)