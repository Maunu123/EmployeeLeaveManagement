from django.apps import AppConfig
from django.db.utils import OperationalError

class LeaveAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Leave_app'

    def ready(self):
        from .models import Employee
        try:
            if not Employee.objects.filter(email='admin@gmail.com').exists():
                Employee.objects.create(
                    first_name='Default',
                    last_name='Admin',
                    email='admin@gmail.com',
                    phone='0000000000',
                    department='Admin',
                    designation='Administrator',
                    employee_type='Admin',
                    password='@123'  # store plain password (can hash later)
                )
        except OperationalError:
            # database not ready yet (ignore migration phase)
            pass
