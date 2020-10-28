# Generated by Django 3.0.5 on 2020-10-20 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tesafe', '0064_systemname_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='webadmin',
            name='alias',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='alias',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tester',
            name='alias',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='webadmin',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='webadmin',
            name='phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='webuser',
            name='alias',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]