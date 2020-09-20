from django.db import models
from django.contrib.auth.models import User


# model of Admin
class WebAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.first_name


# model of Seller
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="none")
    alias = models.CharField(max_length=100, default="none")
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='seller', default="none")
    is_freeze = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


# model of Tester
class Tester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="none")
    alias = models.CharField(max_length=100, default="none")
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='tester', default="none")
    is_freeze = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


#  model of WebUser
class WebUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='user', default="none")

    def __str__(self):
        return self.first_name


# Login Activity model of Admin
class WebAdminLoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_time = models.TimeField(auto_now=True)
    login_date = models.DateField(auto_now=True)
    duration = models.CharField(max_length=50, default="0 minutes")
    device_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'web_login_history'
        verbose_name_plural = 'login history'


# Login Activity model of Admin
class PasswordHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    login_time = models.TimeField(auto_now=True)
    login_date = models.DateField(auto_now=True)
    device_name = models.CharField(max_length=255, null=True)
    last_pass = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'Password History'
        verbose_name_plural = 'Password Histories'


# PWG Server
class PWGServers(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    pwg_count = models.IntegerField()
    transfer_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        verbose_name_plural = "PWG Servers"

    def __str__(self):
        return self.name


# PWGs modal
class PWG(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    owned_by = models.ForeignKey(PWGServers, verbose_name="PWGServers", on_delete=models.CASCADE, null=True)
    transfer_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    is_tested = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "PWGs"

    def __str__(self):
        return self.name


# model for Transfer PWG management
class TransferPwg(models.Model):
    pwg_owner = models.OneToOneField(PWG, on_delete=models.CASCADE, null=True, blank=True)
    pwgs_owner = models.ForeignKey(PWGServers, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Transfer PWG'
        verbose_name_plural = 'Transfer PWGs'


# model for Transfer PWG Server management
class TransferPwgs(models.Model):
    pwgs_owner = models.OneToOneField(PWGServers, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Transfer PWG Server'
        verbose_name_plural = 'Transfer PWG Servers'