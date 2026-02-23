from django.db import models
from django.contrib.auth.hashers import make_password


EMPLOYEE_TYPES = (
    ('Admin', 'Admin'),
    ('HR', 'HR'),
    ('Manager', 'Manager'),
    ('Staff', 'Staff'),
)


class Employee(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    employee_type = models.CharField(
        max_length=20,
        choices=EMPLOYEE_TYPES,
        default='Staff'
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordinates'
    )

    password = models.CharField(max_length=128, default='')
    date_joined = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_type})"


class Leave(models.Model):

    LEAVE_TYPES = [
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )

    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    manager_comment = models.TextField(blank=True, null=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} - {self.leave_type}"


class LeaveBalance(models.Model):

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    sick_days = models.IntegerField(default=20)
    casual_days = models.IntegerField(default=5)
    

    def __str__(self):
        return f"{self.employee} Balance"