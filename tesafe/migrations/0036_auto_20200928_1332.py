# Generated by Django 3.0.5 on 2020-09-28 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0035_webuser_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='webuser',
            name='is_authorized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='webuser',
            name='is_freeze',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='webuser',
            name='is_shared',
            field=models.BooleanField(default=False),
        ),
    ]