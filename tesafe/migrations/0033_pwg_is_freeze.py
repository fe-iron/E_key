# Generated by Django 3.0.5 on 2020-09-23 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0032_pwguserecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwg',
            name='is_freeze',
            field=models.BooleanField(default=False),
        ),
    ]
