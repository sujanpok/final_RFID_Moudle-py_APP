from django import forms
# from django.contrib.auth.models import User
from .models import EmployeeDetail

class UserEditForm(forms.ModelForm):
    class Meta:
        model = EmployeeDetail
        fields = ['full_name', 'date_of_birth', 'address','phone_number','email']
        


class ICNoForm(forms.Form):
    ic_no = forms.CharField(max_length=50, label='IC Number')