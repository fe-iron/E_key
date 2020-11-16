# Generated by Django 3.0.5 on 2020-11-15 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tesafe', '0076_remove_testedpwghistory_tested_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='pwguserecord',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='used_by', to=settings.AUTH_USER_MODEL),
        ),
    ]