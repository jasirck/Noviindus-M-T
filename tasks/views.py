from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import  Task
from .serializers import UserSerializer, TaskSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'


class TaskListCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

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
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        print(pk)
        task = get_object_or_404(Task, pk=pk)
        print(task)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        print(request.data)
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

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    

class UserTaskUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get_object(self, pk, user):
        task = get_object_or_404(Task, pk=pk, assigned_to=user)
        return task

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        allowed_fields = {'status', 'completion_report', 'worked_hours'}

        data = {key: value for key, value in request.data.items() if key in allowed_fields}

        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
