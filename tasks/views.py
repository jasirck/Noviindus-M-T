from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import  Task
from users.models import CustomUser
from .serializers import UserSerializer, TaskSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'ADMIN' or request.user.is_superuser )


class TaskListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self, request, pk):
        print(pk)
        task = get_object_or_404(Task, pk=pk)
        print(task)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)   
        print(task)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response({"detail": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)





    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user
    

class UserTaskListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdmin]
    

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    
class TaskStatusFilterAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        status_param = request.query_params.get('status')
        if status_param:
            tasks = Task.objects.filter(status=status_param.upper())
        else:
            tasks = Task.objects.all()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    

class UserAllTasksAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        print(user, request.user)
        if request.user != user and  not request.user.is_superuser:
            return Response({"detail": "Not authorized to view these tasks."}, status=status.HTTP_403_FORBIDDEN)

        tasks = Task.objects.filter(assigned_to=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class UserTaskDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, task_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        if request.user != user and not request.user.is_staff and not request.user.is_superuser:
            return Response({"detail": "Not authorized to view this task."}, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(Task, pk=task_id, assigned_to=user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, user_id, task_id):
        user = get_object_or_404(CustomUser, pk=user_id)
        if request.user != user and not request.user.is_staff and not request.user.is_superuser:
            return Response({"detail": "Not authorized to update this task."}, status=status.HTTP_403_FORBIDDEN)

        task = get_object_or_404(Task, pk=task_id, assigned_to=user)

        allowed_fields = {'status', 'completion_report', 'worked_hours'}
        data = {key: value for key, value in request.data.items() if key in allowed_fields}

        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
