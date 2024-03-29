# Generated by Django 3.0.5 on 2020-09-30 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tesafe', '0044_auto_20200930_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authorize_to', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pwg', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tesafe.PWG')),
                ('pwgserver', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tesafe.PWGServers')),
            ],
        ),
    ]
