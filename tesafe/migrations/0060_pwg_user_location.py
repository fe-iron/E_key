# Generated by Django 3.0.5 on 2020-10-13 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0059_auto_20201011_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwg',
            name='user_location',
            field=models.CharField(default='T', max_length=2, null=True),
        ),
    ]
