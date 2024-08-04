from django.urls import path
from .views import home, user_login, edit_profile, profile, user_logout,ic_no_input,record_attendance

urlpatterns = [
    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('profile/', profile, name='profile'),
    path('logout/', user_logout, name='logout'),
    path('ic_no_input/', ic_no_input, name='ic_no_input'),
    path('record_attendance/', record_attendance, name='record_attendance'),
]
