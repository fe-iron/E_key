# Generated by Django 3.0.5 on 2020-09-18 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0022_auto_20200918_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='profile_pic',
            field=models.ImageField(default='none', upload_to='seller'),
        ),
    ]