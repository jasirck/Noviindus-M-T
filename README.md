# Task Management Application

## Overview
This application is designed for managing tasks with a feature to submit completion reports when marking a task as completed. The system supports multiple roles: SuperAdmin, Admin, and User, each with different permissions and abilities to manage tasks.

## Features

### User Authentication:
- **JWT Authentication** for secure access to APIs.
- Users can authenticate via username and password, receiving a JWT token for further requests.

### Roles and Permissions:
- **SuperAdmin**: 
    - Can manage admins (create, delete, assign roles, promote/demote).
    - Can manage users (create, delete, update).
    - Has full access to the Admin panel with all privileges.
  
- **Admin**:
    - Can create, assign, view, and manage tasks.
    - Can view task completion reports for tasks assigned to users.
    - Limited access to Admin panel (can manage tasks but not users).
  
- **User**:
    - Can view their assigned tasks, update task status, and submit a completion report (including worked hours).
    - Can only interact with their own tasks via the User API.

### Admin Panel:
- **SuperAdmin Features**:
    - Manage all users, admins, tasks, and view task completion reports.
  
- **Admin Features**:
    - Can assign and manage tasks for their users.
    - Can view task completion reports (including worked hours).

### API Endpoints:
1. **GET /tasks**: Fetch all tasks assigned to the logged-in user.
2. **PUT /tasks/{id}**: Update task status, marking a task as completed and submitting a completion report.
3. **GET /tasks/{id}/report**: Admins and SuperAdmins can view the completion report for a task.

### Task Model Fields:
- **Title**: The task name.
- **Description**: A detailed description of the task.
- **Assigned To**: The user assigned to the task.
- **Due Date**: Task deadline.
- **Status**: Current status of the task (Pending, In Progress, Completed).
- **Completion Report**: A text field for the user to provide a report upon task completion.
- **Worked Hours**: Numeric field to track hours worked on the task.

## Database
- **SQLite** is used as the database for this application.

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/jasirck/Noviindus-M-T.git
    cd Noviindus-M-T

    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Migrations**:
    Run the migrations to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create SuperAdmin User**:
    To create a SuperAdmin user, use the following command:
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the Application**:
    Start the development server:
    ```bash
    python manage.py runserver
    ```
    Once the server is running, open your browser and navigate to:
    http://127.0.0.1:8000/

## API Documentation

The API includes endpoints for:
- Task management (view, update, create, delete).
- User management (create, list, update, delete).
- Task completion report submission (users submit reports after completing tasks).

Make sure to authenticate using the JWT token to access secured endpoints.

## Requirements

- Django
- Django Rest Framework
- djangorestframework-simplejwt (for JWT authentication)
- SQLite (default database)
"""

