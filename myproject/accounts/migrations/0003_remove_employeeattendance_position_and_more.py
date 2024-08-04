# Generated by Django 5.0.7 on 2024-08-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_employeeattendance_ic_no_employeedetail_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeattendance',
            name='position',
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='employee_id',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='employeeattendance',
            name='status',
            field=models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Leave')], max_length=1),
        ),
    ]
