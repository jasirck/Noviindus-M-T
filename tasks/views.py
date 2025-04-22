from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import  Task
from users.models import CustomUser
from .serializers import UserSerializer, TaskSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, CustomUserCreationForm , EditUserForm,UserTaskForm
from django.contrib import messages



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



@login_required
def superadmin_dashboard(request):
    if not request.user.is_superuser:
        logout(request)
        return render(request, "not_authorized.html")

    status_filter = request.GET.get('status')
    tasks = Task.objects.filter(status=status_filter) if status_filter else Task.objects.all()
    form = TaskForm(request.POST or None)
    print(request.POST,'users',form.is_valid(),form.errors )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("superadmin-dashboard")

    return render(request, "dashboard_superadmin.html", {
        "tasks": tasks,
        "form": form,
        "users": CustomUser.objects.all()
    })

@login_required
def admin_dashboard(request):
    tasks = Task.objects.all()  
    users = CustomUser.objects.all()  
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print(form.is_valid(),form.errors)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('admin-dashboard')  

    else:
        form = TaskForm()

    context = {
        'form': form,
        'tasks': tasks,
        'users': users,
    }
    return render(request, 'dashboard_admin.html', context)
@login_required
def user_dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'dashboard_user.html', {'tasks': tasks})


def user_edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    print('user_edit_task',task)
    if request.method == 'POST':
        form = UserTaskForm(request.POST, instance=task)
        print(form.is_valid(),form.errors)
        if form.is_valid():
            task.status = form.cleaned_data['status']
            task.completion_report = form.cleaned_data['completion_report']
            task.worked_hours = form.cleaned_data['worked_hours']
            task.save()
            return redirect('user-dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'user_edit_task.html', {'form': form, 'task': task})


@login_required
def edit_task(request, task_id, from_source):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST or None, instance=task)
    users = CustomUser.objects.filter(role='USER')
    if request.method == "POST" and form.is_valid():
        form.save()
        if from_source == 'admin':
            return redirect("admin-dashboard")
        elif from_source == 'superadmin':
            return redirect("superadmin-dashboard")
        else:
            return redirect("user-dashboard")

    return render(request, "edit_task.html", {"form": form, "task": task, "users": users})


@login_required
def delete_task(request, task_id, from_source):
    task = get_object_or_404(Task, pk=task_id)
    
    # Check permissions
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        logout(request)
        return render(request, "not_authorized.html")

    if request.method == "POST":
        task.delete()
        if from_source == 'admin':
            return redirect("admin-dashboard")
        elif from_source == 'superadmin':
            return redirect("superadmin-dashboard")

    return render(request, "confirm_delete.html", {
        "object": task, 
        "type": "task",
        "from_source": from_source
    })


@login_required
def add_user(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        logout(request)
        return render(request, "not_authorized.html")

    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("superadmin-dashboard")
    return render(request, "add_user.html", {"form": form})

@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        logout(request)
        return render(request, "not_authorized.html")

    user = get_object_or_404(CustomUser, pk=user_id)
    form = EditUserForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect("superadmin-dashboard")

    return render(request, "edit_user.html", {"form": form, "user": user})

def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.user.is_superuser:
        user.delete()
        messages.success(request, "User deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete users.")

    return redirect('superadmin-dashboard')  # Redirect to the dashboard or user management page