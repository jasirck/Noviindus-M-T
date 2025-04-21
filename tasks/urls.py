from django.urls import path
from . import views
from .views import (
    superadmin_dashboard,
    admin_dashboard,
    user_dashboard,
    edit_task,
    delete_task
)

urlpatterns = [    
    path('list/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('list/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail'),
    path('user/', views.UserTaskListAPIView.as_view(), name='user-tasks'),
    path('user/<int:user_id>/' , views.UserAllTasksAPIView.as_view(), name='user-tasks-all'),
    path('user/<int:user_id>/tasks/<int:task_id>/', views.UserTaskDetailAPIView.as_view(), name='user-task-detail'),
    path('status/', views.TaskStatusFilterAPIView.as_view(), name='task-status-filter'),
    path("dashboard/superadmin/", superadmin_dashboard, name="superadmin-dashboard"),
    path("dashboard/user/", user_dashboard, name="user-dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin-dashboard"),
    path("tasks/<int:task_id>/<str:from_source>/edit/", edit_task, name="edit-task"),
    path("tasks/<int:task_id>/<str:from_source>/delete/", delete_task, name="delete-task"),
    path('admin/add-user/', views.add_user, name='add-user'),
    path('admin/edit-user/<int:user_id>/', views.edit_user, name='edit-user'),

]
