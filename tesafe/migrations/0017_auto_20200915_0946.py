# Generated by Django 3.0.5 on 2020-09-15 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0016_auto_20200915_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='profile_pic',
            field=models.ImageField(upload_to='seller'),
        ),
    ]
