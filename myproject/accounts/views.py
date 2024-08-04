from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from django.conf import settings
from .forms import UserEditForm
from .forms import ICNoForm
from .models import EmployeeDetail,EmployeeAttendance
from django.contrib import messages
from django.utils import timezone
import pytz
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger('django')


def home(request):
    current_year = datetime.now().year
    return render(request, 'home.html', {
        'current_year': current_year,
        'company_name': settings.COMPANY_NAME,
    })


def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin:index')  # Redirect to Django admin index page
            else:
                return redirect('profile')  # Redirect to user profile page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def edit_profile(request):
    user = request.user
    
    try:
        # Retrieve the employee detail for the current user
        employee = EmployeeDetail.objects.get(user=user)
    except EmployeeDetail.DoesNotExist:
        # Handle the case where there is no EmployeeDetail for this user
        employee = None
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=employee)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def profile(request):
    
    # Get the current user
    user = request.user

    try:
        # Retrieve the employee detail for the current user
        employee = EmployeeDetail.objects.get(user=user)
        
    except EmployeeDetail.DoesNotExist:
        # Handle the case where there is no EmployeeDetail for this user
        employee = None
        
    return render(request, 'profile.html', {'employeeID': employee})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def ic_no_input(request):
    if request.method == 'POST':
        form = ICNoForm(request.POST)
        if form.is_valid():
            ic_no = form.cleaned_data['ic_no']
            
            try:
                # Retrieve employee details using IC_No
                employee = EmployeeDetail.objects.get(IC_No=ic_no)
                
                # Get the current time
                now = timezone.now()
                
                # Convert UTC time to local time
                local_timezone = pytz.timezone('Asia/Tokyo')  # Replace with your desired timezone
                local_time = now.astimezone(local_timezone)
                
                # Check all attendance records for the given employee
                records = EmployeeAttendance.objects.filter(
                    employee_id=employee.employee_id
                )
                
                # Flag to determine if any record with status 'I' was found
                found_incomplete = False
                
                for record in records:
                    if record.status == 'I':
                        # Update the existing record's end time and status
                        record.end_time = local_time.time()
                        record.status = 'O'
                        record.save()
                        found_incomplete = True
                
                if not found_incomplete:
                    # No record with status 'I' was found, so create a new one
                    EmployeeAttendance.objects.create(
                        employee_id=employee.employee_id,
                        date=local_time.date(),
                        start_time=local_time.time(),
                        end_time=None,  # Placeholder, should be updated when the user checks out
                        status='I',
                        IC_No=ic_no
                    )
                
                # Add a success message
                messages.success(request, 'Attendance recorded successfully.')
                
                # Redirect to a success page or the same page
                return redirect('ic_no_input')
                
            except EmployeeDetail.DoesNotExist:
                # Handle the case where IC_No is not found
                form.add_error('ic_no', 'Employee with this IC Number does not exist.')
    else:
        form = ICNoForm()

    return render(request, 'ic_no_input.html', {'form': form})


#for RFID reader
@csrf_exempt  # Temporarily disable CSRF for API (use authentication in production)
def record_attendance(request):
    if request.method == 'POST':
        try:
            # Extract IC number from the request body
            body = json.loads(request.body)
            ic_no = body.get('ic_no')
            logger.debug('This is a debug message:',ic_no)
            if not ic_no:
                return JsonResponse({'error': 'IC No is requireds.'}, status=400)
            
            # Retrieve employee details using IC_No
            employee = EmployeeDetail.objects.get(IC_No=ic_no)
            
            # Get the current time
            now = timezone.now()
            
            # Convert UTC time to local time
            local_timezone = pytz.timezone('Asia/Tokyo')  # Replace with your desired timezone
            local_time = now.astimezone(local_timezone)
            
            # Check all attendance records for the given employee
            records = EmployeeAttendance.objects.filter(employee_id=employee.employee_id)
            
            # Flag to determine if any record with status 'I' was found
            found_incomplete = False
            
            for record in records:
                if record.status == 'I':
                    # Update the existing record's end time and status
                    record.end_time = local_time.time()
                    record.status = 'O'
                    record.save()
                    found_incomplete = True
            
            if not found_incomplete:
                # No record with status 'I' was found, so create a new one
                EmployeeAttendance.objects.create(
                    employee_id=employee.employee_id,
                    date=local_time.date(),
                    start_time=local_time.time(),
                    end_time=None,  # Placeholder, should be updated when the user checks out
                    status='I',
                    IC_No=ic_no
                )
            
            return JsonResponse({'message': 'Attendance recorded successfully.'})
            
        except EmployeeDetail.DoesNotExist:
            # Handle the case where IC_No is not found
            return JsonResponse({'error': 'Employee with this IC Number does not exist.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)