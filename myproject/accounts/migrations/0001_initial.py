# Generated by Django 5.0.7 on 2024-08-04 09:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Leave'), ('T', 'Late'), ('E', 'Early Leave')], max_length=1)),
                ('position', models.CharField(max_length=50)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
