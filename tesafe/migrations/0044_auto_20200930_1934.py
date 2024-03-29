# Generated by Django 3.0.5 on 2020-09-30 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0043_authorize'),
    ]

    operations = [
        migrations.AddField(
            model_name='authorize',
            name='pwgserver',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tesafe.PWGServers'),
        ),
        migrations.AddField(
            model_name='pwg',
            name='is_authorized',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pwg',
            name='is_shared',
            field=models.BooleanField(default=False),
        ),
    ]
