from django.contrib import admin
from .models import Employee, Leave, LeaveBalance



class LeaveBalanceInline(admin.StackedInline):
    model = LeaveBalance
    extra = 0
    can_delete = False



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'employee_type',
        'department',
        'designation',
        'manager',
        'date_joined',
    )

    list_filter = ('employee_type', 'department')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-date_joined',)

    inlines = [LeaveBalanceInline]



@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'leave_type',
        'start_date',
        'end_date',
        'status',
        'approved_by',
        'applied_on',
    )

    list_filter = ('leave_type', 'status')
    search_fields = (
        'employee__first_name',
        'employee__last_name',
        'employee__email'
    )
    ordering = ('-applied_on',)



@admin.register(LeaveBalance)
class LeaveBalanceAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'sick_days',
        'casual_days',
        
    )