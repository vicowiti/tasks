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

### System Architecture

flowchart TD

    subgraph Client["Frontend / API Consumer"]
        A1["Login Request"]
        A2["API Requests (Tasks, Users, etc.)"]
    end

    subgraph Django["Django REST Framework Backend"]

        subgraph Auth["Authentication Layer"]
            B1["JWT Login Endpoint"]
            B2["Access Token (1 hr)"]
            B3["Refresh Token (7 days)"]
            B4["Change Default Password Endpoint"]
        end

        subgraph Users["User Management"]
            C1["UserViewSet"]
            C2["Role Logic: Admin / Manager / Member"]
            C3["Permission Classes"]
        end

        subgraph Tasks["Task Management"]
            D1["TaskViewSet"]
            D2["Role-Based Queryset Filtering"]
            D3["/tasks/by-user/<id> Endpoint"]
            D4["Task Assignment Rules"]
        end

        subgraph Docs["Documentation"]
            E1["drf-spectacular"]
            E2["OpenAPI Schema"]
            E3["Swagger UI /api/docs/"]
        end
    end


    subgraph DB["PostgreSQL Database"]
        F1["Users Table"]
        F2["Tasks Table"]
        F3["Relations: assignee → User, created_by → User"]
    end

    subgraph Deployment["Nginx + Gunicorn Server"]
        G1["Gunicorn (WSGI App Server)"]
        G2["Unix Socket Communication"]
        G3["Nginx Reverse Proxy"]
    end


    %% Connections

    Client -->|"Sends Credentials"| B1
    B1 -->|"Returns JWT Tokens"| Client

    Client -->|"Sends Bearer Token"| Django
    Django -->|"Performs DB Queries"| DB

    Auth --> Users
    Auth --> Tasks
    Users --> DB
    Tasks --> DB

    Django -->|"Served via Unix Socket"| G1
    G1 -->|"Reverse Proxied"| G3
    G3 -->|"Public API"| Client
