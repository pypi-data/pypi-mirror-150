from django.contrib import admin
from .models import Post, Login, AlertMessage

# Register your models here.

admin.site.register(Post)
admin.site.register(Login)
admin.site.register(AlertMessage)
