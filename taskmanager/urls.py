from django.contrib import admin
from django.urls import path, include
from users.views import (
    custom_login,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path("", custom_login, name="custom-login"),
]
