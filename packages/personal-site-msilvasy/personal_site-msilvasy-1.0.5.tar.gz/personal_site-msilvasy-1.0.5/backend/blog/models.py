from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    post = models.TextField()
    date = models.CharField(max_length=10)
    name = models.TextField()
    username = models.TextField(default='')

    def __str__(self):
        return self.title

class Login(models.Model):
    username = models.TextField(default='')
    date = models.CharField(max_length=10)

    def __str__(self):
        return self.username + ' log in on ' + self.date

class AlertMessage(models.Model):
    message = models.CharField(max_length=100)
    uuid = models.TextField(default='')
    category = models.CharField(max_length=25, default='')

    def __str__(self):
        return self.message
