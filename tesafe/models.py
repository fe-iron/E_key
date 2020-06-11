from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

getUser = get_user_model()

#
# class User(AbstractUser):
#     is_webAdmin = models.BooleanField(default=False)
#     is_seller = models.BooleanField(default=False)
#     is_tester = models.BooleanField(default=False)
#     is_user = models.BooleanField(default=False)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#
#
# class Seller(models.Model):
#     name = models.ForeignKey(getUser, related_name='first_name', on_delete=models.CASCADE)
#
#     email = models.CharField(max_length=150)
#     phone = models.CharField(max_length=12)
#
#
# class WebAdmin(models.Model):
#     name = models.ForeignKey(getUser, related_name='first_name', on_delete=models.CASCADE)
#     email = models.CharField(max_length=150)
#     phone = models.CharField(max_length=12)