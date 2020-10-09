# Generated by Django 3.0.5 on 2020-09-27 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0033_pwg_is_freeze'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='user_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='webuser',
            name='associated_with',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tesafe.Seller'),
        ),
    ]