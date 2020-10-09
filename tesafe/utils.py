import random
import datetime
from six import text_type
from .models import SystemName
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def unique_name(accType, nnn):
    instance = datetime.datetime.now()
    national_code = nnn
    year = str(instance.year)
    month = instance.month
    day = instance.day
    hour = instance.hour
    serial_no = str(random.randint(1000,9999))
    if SystemName.objects.filter(serial_no=serial_no).exists():
        return "Something went wrong try again"
    else:
        name = accType
        name += national_code
        name += year
        if month <= 9:
            month = str(month)
            month = '0'+month
        else:
            month = str(month)
        name += month
        if day <=9:
            day = str(day)
            day = '0' + day
        else:
            day = str(day)
        name += day
        if hour <= 9:
            hour = str(hour)
            hour = '0' + hour
        else:
            hour = str(hour)
        name += hour

        name += serial_no
        return name


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()