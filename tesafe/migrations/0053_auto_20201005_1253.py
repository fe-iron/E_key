# Generated by Django 3.0.5 on 2020-10-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0052_auto_20201005_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwg',
            name='is_tested_faulty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pwg',
            name='is_tested_good',
            field=models.BooleanField(default=False),
        ),
    ]