# Generated by Django 3.0.5 on 2020-09-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0013_passwordhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordhistory',
            name='device_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
