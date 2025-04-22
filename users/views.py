from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, get_user_model,login
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from .models import CustomUser
from django.contrib import messages


User = get_user_model()


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        print("is_superuser",request.user.is_superuser)
        return request.user.is_authenticated and request.user.is_superuser



def custom_login(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]
        except KeyError as e:
            messages.error(request, f"Missing field: {e}")
            return redirect('custom-login')  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("superadmin-dashboard")
            elif user.role == "ADMIN":
                return redirect("admin-dashboard")
            else:
                return redirect("user-dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")


class ObtainTokenPairView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.role,
                "is_superuser": user.is_superuser
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]


    def post(self, request):
    # Only SUPERADMIN can assign roles
        if request.user.is_authenticated and  request.user.is_superuser:
            return Response({"detail": "You are not allowed to assign roles."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

class UserDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        if  user.is_superuser:
            return Response({"detail": "Cannot delete a SuperAdmin."}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperAdmin]

    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
