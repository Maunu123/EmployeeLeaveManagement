"""
URL configuration for EmployeeLeaveManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from Leave_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('employee_dashboard/', employee_dashboard, name='employee_dashboard'),
    
    path('edit_employee/<int:emp_id>/', edit_employee, name='edit_employee'),
    path('delete_employee/<int:emp_id>/',delete_employee , name='delete_employee'),
    
    path('apply_leave/', apply_leave, name='apply_leave'),
    path('manage_leave/', manage_leave, name='manage_leave'),
    path('calendar/', leave_calendar, name='leave_calendar'),
]