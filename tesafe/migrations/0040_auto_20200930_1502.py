# Generated by Django 3.0.5 on 2020-09-30 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0039_auto_20200930_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systemname',
            name='serial_no',
            field=models.CharField(max_length=4),
        ),
    ]
