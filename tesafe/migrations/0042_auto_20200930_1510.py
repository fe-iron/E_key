# Generated by Django 3.0.5 on 2020-09-30 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0041_systemname_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pwgservers',
            name='name',
        ),
        migrations.AddField(
            model_name='pwgservers',
            name='system_name',
            field=models.CharField(default='not assigned', max_length=19, null=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='system_name',
            field=models.CharField(default='not assigned', max_length=19, null=True),
        ),
        migrations.AddField(
            model_name='tester',
            name='system_name',
            field=models.CharField(default='not assigned', max_length=19, null=True),
        ),
        migrations.AddField(
            model_name='webuser',
            name='system_name',
            field=models.CharField(default='not assigned', max_length=19, null=True),
        ),
    ]