# 🏢 Employee Leave Management System

A Django-based web application to manage employees, leave applications, approvals, and leave balance tracking with role-based access control.

---

## 🚀 Features

- 🔐 Secure Login & Logout
- 👤 Employee Management (Add / Edit / Delete)
- 🏢 Role-Based Access (Admin / HR / Manager / Staff)
- 📝 Apply Leave
- ✅ Approve / Reject Leave Requests
- 📊 Automatic Leave Balance Calculation
- 📅 Leave Calendar View
- 🛠 Django Admin Panel Support

---

## 🛠 Tech Stack

- Python 3.x
- Django
- MySQl
- HTML5
- CSS3
- Bootstrap

---

## 📂 Project Structure

EmployeeLeaveManagement/
│
├── manage.py
├── requirements.txt
│
├── templates/
│ ├── login.html
│ └── admin_dashboard.html and other
│
│
├── EmployeeLeaveManagement/
│ ├── **init**.py
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
│
└── Leave_app/
├── **init**.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── urls.py
├── migrations/
│ └── **init**.py

---

## ⚙️ Installation & Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Maunu123/EmployeeLeaveManagement.git
cd EmployeeLeaveManagement
```

Activate the virtual environment:

#### Windows:

```
venv\Scripts\activate
```

#### Mac/Linux:

```
source venv/bin/activate
```

3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

4️⃣ Apply Migrations

```
python manage.py makemigrations
python manage.py migrate
```

5️⃣ Create Superuser

```
python manage.py createsuperuser
```

6️⃣ Run Development Server

```
python manage.py runserver

Open in browser:

http://127.0.0.1:8000/
```

#### Django Admin Panel:

```
http://127.0.0.1:8000/admin/
```

## User Roles

### Admin

- Add / Update / Delete Employees
- Assign Managers

### Employee

- Approve / Reject Leave Requests
- View Team Leave Status
- Apply for Leave
- Track Leave Status
- View Leave Balance

### Database Models

- Employee
- Leave
- LeaveBalance

---
