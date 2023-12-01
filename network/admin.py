from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ("creator","content","date")

admin.site.register(User)
admin.site.register(Post, PostAdmin)