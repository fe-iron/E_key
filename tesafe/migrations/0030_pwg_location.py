# Generated by Django 3.0.5 on 2020-09-23 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0029_auto_20200922_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwg',
            name='location',
            field=models.CharField(default='A', max_length=2),
        ),
    ]