# Generated by Django 3.0.5 on 2020-09-30 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0045_share'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='authorize_to',
            new_name='share_to',
        ),
    ]
