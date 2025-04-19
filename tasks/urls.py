from django.urls import path
from . import views

urlpatterns = [    
    path('list/', views.TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('list/<int:pk>/', views.TaskDetailAPIView.as_view(), name='task-detail'),
     path('user/', views.UserTaskListAPIView.as_view(), name='user-tasks'),
    path('user/<int:pk>/', views.UserTaskUpdateAPIView.as_view(), name='user-task-detail'),
]
