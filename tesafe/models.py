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
    alias = models.CharField(max_length=100, default="none", null=True)
    profile_pic = models.ImageField(upload_to='user/', default="none")
    associated_with = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, default=None)
    is_freeze = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name


class UserToUser(models.Model):
    main_user = models.ForeignKey(WebUser, on_delete=models.SET_NULL, null=True, default=None, related_name="main_user")
    associated_user = models.ForeignKey(WebUser, on_delete=models.SET_NULL, null=True, default=None, related_name="associated_user")
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User to User Association"
        verbose_name_plural = "User to User Associations"


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
    # T = obtained by Transfer can do all operation
    # A = means PWG is authorized by the other User or Seller can do get PW, rev record
    # DA =  means the PWG has been authorized to the other User can do de-authorize
    # s =  means the PWG is shared by the other User or Seller, only Get PW. and Review rec. are available
    # DS = means the PWG has been share to the other User, Get PW. and Review rec. and De-share are available

    user_location = models.CharField(max_length=2, null=True, default="T")
    is_freeze = models.BooleanField(default=False)
    is_authorized = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    is_tested_good = models.BooleanField(default=False)
    # if failed comes here
    is_tested_faulty = models.BooleanField(default=False)
    # it will get active when a seller transfer to user
    sold_from = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name="sold", blank=True)

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
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    password = models.CharField(max_length=255)
    pwg = models.ForeignKey(PWG, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return str(self.date)

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
    system_name = models.CharField(max_length=19, null=True, default="not assigned")
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


class PWGHistory(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    object = models.ForeignKey(User, on_delete=models.SET("object Deleted"), null=True, default=None, related_name="authorize_to")
    pwg = models.ForeignKey(PWG, on_delete=models.SET("object Deleted"), null=True, default=None, related_name="pwg")
    # N = None, A = Authorize, S = Share, T = Transfer, DA = De-authorize, DS = De-share, D = Deleted,
    # AD = buy from admin, RAD = Return to Admin, RT = Return to Testing again, P = Pass, F = Fail
    action = models.CharField(default="N", max_length=3)

    class Meta:
        verbose_name = "PWG History"
        verbose_name_plural = "PWG Histories"


class TesterPWGHistory(models.Model):
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    pwg_name = models.ForeignKey(PWG, on_delete=models.SET_NULL, null=True)
    got_on = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = "Tester PWG Testing History"
        verbose_name_plural = "Tester PWG Testing Histories"

