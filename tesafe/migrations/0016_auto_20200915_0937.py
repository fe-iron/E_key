# Generated by Django 3.0.5 on 2020-09-15 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0015_auto_20200914_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='seller'),
        ),
        migrations.AddField(
            model_name='tester',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='tester'),
        ),
        migrations.AddField(
            model_name='webuser',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='user'),
        ),
    ]
