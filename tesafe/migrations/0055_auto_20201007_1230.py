# Generated by Django 3.0.5 on 2020-10-07 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0054_testerpwghistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testerpwghistory',
            name='pwg_history',
        ),
        migrations.AddField(
            model_name='testerpwghistory',
            name='got_on',
            field=models.DateTimeField(default='0001-01-01'),
        ),
    ]