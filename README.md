# Team Task Management System (Django REST Framework)

A role-based task management backend built with **Django 5**, **Django REST Framework**, **PostgreSQL**, **JWT authentication**, and **Swagger documentation**.

This system supports:

- Admin, Manager, and Member roles
- Role-based task visibility
- Task assignment flow
- Custom password change endpoint
- Complete Swagger API documentation

---

## ## ⚙️ Features

### 🔐 Authentication

- JWT (access + refresh tokens)
- Access token: **60 minutes**
- Refresh token: **7 days**
- Login response returns:
  - First Name
  - Last Name
  - Role
  - `has_default_password` flag

### 👥 Roles

| Role        | Capabilities                               |
| ----------- | ------------------------------------------ |
| **Admin**   | Full control: manage users + tasks         |
| **Manager** | Manage tasks, assign tasks, view all tasks |
| **Member**  | View only own tasks, cannot assign tasks   |

### 📌 Task Rules

- Admin + Manager → access to ALL tasks
- Member → only tasks assigned to them
- Managers/Admins can fetch tasks by user, assign and delete tasks
