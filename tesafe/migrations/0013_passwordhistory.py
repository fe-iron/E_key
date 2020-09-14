# Generated by Django 3.0.5 on 2020-09-14 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tesafe', '0012_auto_20200914_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.TimeField(auto_now=True)),
                ('login_date', models.DateField(auto_now=True)),
                ('device_name', models.CharField(max_length=255)),
                ('last_pass', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Password History',
                'verbose_name_plural': 'Password Histories',
            },
        ),
    ]