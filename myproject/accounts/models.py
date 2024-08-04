from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import logging
logger = logging.getLogger('django')

logger.debug('This is a debug message')

class EmployeeDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=15, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    date_joined = models.DateField()
    IC_No = models.CharField(max_length=50, default="UNKNOWN")

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = EmployeeDetail.objects.all().order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id.split('ATD')[-1])
                self.employee_id = f'ATD{last_id + 1:04d}'
            else:
                self.employee_id = 'ATD0001'
        super(EmployeeDetail, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

class EmployeeAttendance(models.Model):
    STATUS_CHOICES = [
        ('I', 'IN'),
        ('O', 'OUT'),
    ]

    id = models.AutoField(primary_key=True)
    employee_id = models.CharField(max_length=15)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    IC_No = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.employee_id} - {self.date} - {self.status}"
