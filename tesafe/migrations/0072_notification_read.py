# Generated by Django 3.0.5 on 2020-11-09 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0071_notification_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
