# Generated by Django 5.0.7 on 2024-08-04 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_employeeattendance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]