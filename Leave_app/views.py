from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Employee, Leave, LeaveBalance
from django.contrib.auth.hashers import make_password
import json
from datetime import datetime, timedelta
from functools import wraps




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            emp = Employee.objects.get(email=email)

            if check_password(password, emp.password):
                request.session['employee_id'] = emp.id

                if emp.employee_type == 'Admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('employee_dashboard')
            else:
                messages.error(request, "Invalid Password")

        except Employee.DoesNotExist:
            messages.error(request, "Invalid Email")

    return render(request, 'login.html')



def logout_view(request):
    request.session.flush()
    return redirect('login')



def admin_dashboard(request):
    if 'employee_id' not in request.session:
        return redirect('login')

    try:
        admin_user = Employee.objects.get(id=request.session['employee_id'])
    except Employee.DoesNotExist:
        return redirect('login')

    
    if admin_user.employee_type != 'Admin':
        return redirect('employee_dashboard')

    if request.method == 'POST':

        email = request.POST.get('email')

        if Employee.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            emp = Employee.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=email,
                phone=request.POST.get('phone'),
                department=request.POST.get('department'),
                designation=request.POST.get('designation'),
                employee_type=request.POST.get('employee_type'),
                manager_id=request.POST.get('manager') or None,
                password=make_password(request.POST.get('password')),
            )

            LeaveBalance.objects.create(employee=emp)

            messages.success(request, "Employee Added Successfully!")

    employees = Employee.objects.exclude(employee_type='Admin')
    managers = Employee.objects.exclude(employee_type='Staff')

    return render(request, 'admin_dashboard.html', {
        'employees': employees,
        'managers': managers
    })


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        emp_id = request.session.get('employee_id')

        if not emp_id:
            return redirect('login')

        if not Employee.objects.filter(id=emp_id).exists():
            request.session.flush()
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper


def employee_dashboard(request):
    if 'employee_id' not in request.session:
        return redirect('login')

    employee = Employee.objects.get(id=request.session['employee_id'])
    leaves = Leave.objects.filter(employee=employee)
    balance = LeaveBalance.objects.get(employee=employee)

    return render(request, 'employee_dashboard.html', {
        'employee': employee,
        'leaves': leaves,
        'balance': balance
    })



def apply_leave(request):
    if 'employee_id' not in request.session:
        return redirect('login')
    
   

    employee = Employee.objects.get(id=request.session['employee_id'])
    print(employee)

    if request.method == 'POST':
        approver = employee.manager

        Leave.objects.create(
            employee=employee,
            approved_by=approver,
            leave_type=request.POST.get('leave_type'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            reason=request.POST.get('reason'),
        )

        return redirect('employee_dashboard')

    return render(request, 'apply_leave.html')



def manage_leave(request):
    if 'employee_id' not in request.session:
        return redirect('login')

    approver = Employee.objects.get(id=request.session['employee_id'])

    leaves = Leave.objects.filter(approved_by=approver, status='Pending')

    if request.method == 'POST':
        leave = Leave.objects.get(id=request.POST.get('leave_id'))
        action = request.POST.get('action')

        if action == 'Approve':
            leave.status = 'Approved'

            days = (leave.end_date - leave.start_date).days + 1
            balance = LeaveBalance.objects.get(employee=leave.employee)

            if leave.leave_type == 'Sick':
                balance.sick_days -= days
            elif leave.leave_type == 'Casual':
                balance.casual_days -= days

            balance.save()
        else:
            leave.status = 'Rejected'

        leave.save()
        return redirect('manage_leave')

    return render(request, 'manage_leave.html', {'leaves': leaves})



@login_required
def leave_calendar(request):
    leaves = Leave.objects.all()
    events = []

    for leave in leaves:
        events.append({
            "title": f"{leave.employee.first_name} - {leave.leave_type}",
            "start": leave.start_date.strftime("%Y-%m-%d"),
            "end": (leave.end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": leave.status,
        })

    return render(request, "calendar.html", {
        "events_json": json.dumps(events)
    })



def edit_employee(request, emp_id):
    if 'employee_id' not in request.session:
        return redirect('login')

    admin_user = Employee.objects.get(id=request.session['employee_id'])

    # Only Admin can edit
    if admin_user.employee_type != 'Admin':
        return redirect('employee_dashboard')

    employee = get_object_or_404(Employee, id=emp_id)

    if request.method == 'POST':
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.phone = request.POST.get('phone')
        employee.department = request.POST.get('department')
        employee.designation = request.POST.get('designation')
        employee.employee_type = request.POST.get('employee_type')
        employee.manager_id = request.POST.get('manager')

        # If password changed
        new_password = request.POST.get('password')
        if new_password:
            employee.password = make_password(new_password)

        employee.save()
        return redirect('admin_dashboard')

    managers = Employee.objects.exclude(employee_type='Staff')

    return render(request, 'edit_employee.html', {
        'employee': employee,
        'managers': managers
    })

def delete_employee(request, emp_id):
    if 'employee_id' not in request.session:
        return redirect('login')

    admin_user = Employee.objects.get(id=request.session['employee_id'])
    if admin_user.employee_type != 'Admin':
        return redirect('employee_dashboard')

    employee = get_object_or_404(Employee, id=emp_id)

    if employee.id == admin_user.id:
        return redirect('admin_dashboard')

    employee.delete()
    return redirect('admin_dashboard')
