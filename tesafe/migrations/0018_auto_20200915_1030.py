# Generated by Django 3.0.5 on 2020-09-15 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0017_auto_20200915_0946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='webadminloginhistory',
            options={'verbose_name': 'web_login_history', 'verbose_name_plural': 'login history'},
        ),
    ]