from django.urls import path
from . import views

urlpatterns = [    
    path('list/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('list/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail'),
    path('user/', views.UserTaskListAPIView.as_view(), name='user-tasks'),
    path('user/<int:user_id>/' , views.UserAllTasksAPIView.as_view(), name='user-tasks-all'),
    path('user/<int:user_id>/tasks/<int:task_id>/', views.UserTaskDetailAPIView.as_view(), name='user-task-detail'),
    path('status/', views.TaskStatusFilterAPIView.as_view(), name='task-status-filter'),


]
