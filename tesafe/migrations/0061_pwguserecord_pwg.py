# Generated by Django 3.0.5 on 2020-10-13 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0060_pwg_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwguserecord',
            name='pwg',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tesafe.PWG'),
        ),
    ]