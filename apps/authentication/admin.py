from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom User Admin"""

    model = CustomUser
    list_display = ['username', 'email', 'github_username', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'github_username']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('avatar_url', 'bio', 'github_username')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'avatar_url', 'bio', 'github_username')
        }),
    )