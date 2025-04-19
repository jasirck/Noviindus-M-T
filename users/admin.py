# admin.py in users app
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.role == 'SUPERADMIN'

    def has_view_permission(self, request, obj=None):
        return request.user.role == 'SUPERADMIN'

    def has_change_permission(self, request, obj=None):
        return request.user.role == 'SUPERADMIN'

    def has_delete_permission(self, request, obj=None):
        return request.user.role == 'SUPERADMIN'

admin.site.register(CustomUser, CustomUserAdmin)
