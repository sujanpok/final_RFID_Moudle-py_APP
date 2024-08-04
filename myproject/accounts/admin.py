from django.contrib import admin
from .models import EmployeeAttendance
from .models import EmployeeDetail

class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'date', 'start_time', 'end_time', 'status']
    fields = ['employee_id', 'date', 'start_time', 'end_time', 'status']
    list_filter = ['status', 'date']
    search_fields = ['employee_id__username']

admin.site.register(EmployeeAttendance, EmployeeAttendanceAdmin)

class EmployeeDetailAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'date_of_birth', 'address', 'phone_number', 'email', 'position', 'department', 'date_joined', 'IC_No']
    fields = ['user', 'full_name', 'date_of_birth', 'address', 'phone_number', 'email', 'position', 'department', 'date_joined', 'IC_No']
    list_filter = ['position', 'department', 'date_joined']
    search_fields = ['user__username', 'full_name', 'position', 'department']

admin.site.register(EmployeeDetail, EmployeeDetailAdmin)
