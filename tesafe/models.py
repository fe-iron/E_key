from django.db import models
from django.contrib.auth.models import User


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_time = models.TimeField(auto_now=True)
    login_date = models.DateField(auto_now=True)
    duration = models.CharField(max_length=50, default="0 minutes")
    device_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'web_login_history'
        verbose_name_plural = 'webAdmin login history'


# Login Activity model of Admin
class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.TimeField(auto_now=True)
    login_date = models.DateField(auto_now=True)
    device_name = models.CharField(max_length=255, null=True)
    last_pass = models.CharField(max_length=255)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Password History'
        verbose_name_plural = 'Password Histories'


# PWG Server
class PWGServers(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    pwg_count = models.IntegerField()

    class Meta:
        verbose_name_plural = "PWG Servers"

    def __str__(self):
        return self.name


# PWGs modal
class PWG(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    owned_by = models.ForeignKey(PWGServers, verbose_name="PWGServers", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "PWGs"

    def __str__(self):
        return self.name

