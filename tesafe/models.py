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
    system_name = models.CharField(max_length=19, null=True, default="not assigned")
    alias = models.CharField(max_length=100, default="none")
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='seller/', default="none")
    is_freeze = models.BooleanField(default=False)
    user_count = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name


# model of Tester
class Tester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="none")
    system_name = models.CharField(max_length=19, null=True, default="not assigned")
    alias = models.CharField(max_length=100, default="none")
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='tester/', default="none")
    is_freeze = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


#  model of WebUser
class WebUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    system_name = models.CharField(max_length=19, null=True, default="not assigned")
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    alias = models.CharField(max_length=100, default="none")
    profile_pic = models.ImageField(upload_to='user/', default="none")
    associated_with = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, default=None)
    is_freeze = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)

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
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255, default=None, null=True)
    password = models.CharField(max_length=255, default=None, null=True)
    pwg_count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
    system_name = models.CharField(max_length=19, null=True, default="not assigned")

    class Meta:
        verbose_name_plural = "PWG Servers"

    def __str__(self):
        return self.alias


# PWGs modal
class PWG(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    owned_by = models.ForeignKey(PWGServers, verbose_name="PWGServers", on_delete=models.CASCADE, null=True)
    transfer_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=1)
    is_tested = models.BooleanField(default=False)
    location = models.CharField(max_length=2, default='A')
    is_freeze = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)

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


# PWG Use record
class PwgUseRecord(models.Model):
    count = models.IntegerField()
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.date

    class Meta:
        verbose_name = "PWG Use Record"
        verbose_name_plural = "PWG Use Records"


# models for generating system name
class SystemName(models.Model):
    is_user = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_tester = models.BooleanField(default=False)
    is_pwgs = models.BooleanField(default=False)
    serial_no = models.CharField(max_length=4)
    system_name = models.CharField(max_length=19, null=False, default="not assigned")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)


# model for authorize
class Authorize(models.Model):
    pwg = models.ForeignKey(PWG, on_delete=models.CASCADE, default=None)
    authorize_to = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    pwgserver = models.ForeignKey(PWGServers, on_delete=models.CASCADE, default=None)


# model for authorize
class Share(models.Model):
    pwg = models.ForeignKey(PWG, on_delete=models.CASCADE, default=None)
    share_to = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    pwgserver = models.ForeignKey(PWGServers, on_delete=models.CASCADE, default=None)
