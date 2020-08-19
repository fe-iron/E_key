
from django.db import models
from django.contrib.auth.models import User


# class User(AbstractUser):
#     is_webAdmin = models.BooleanField(default=False)
#     is_seller = models.BooleanField(default=False)
#     is_tester = models.BooleanField(default=False)
#     is_user = models.BooleanField(default=False)


# class Seller(models.Model):
#     name = models.ForeignKey(getUser, related_name='first_name', on_delete=models.CASCADE)
#
#     email = models.CharField(max_length=150)
#     phone = models.CharField(max_length=12)


class WebAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name


class Tester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name


class WebUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name


# Login Activity model of Admin
class WebAdminLoginHistory(models.Model):
    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    duration = models.CharField(max_length=50, default="0 minutes")
    device_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'web_login_history'
        verbose_name_plural = 'webAdmin login history'
