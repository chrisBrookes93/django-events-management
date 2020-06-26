from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('email', 'is_staff', 'is_active', 'date_joined')
    ordering = ('email',)
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )


admin.site.register(User, CustomUserAdmin)
