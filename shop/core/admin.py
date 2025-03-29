from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin): 
    model = CustomUser
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'city', 'state', 'address', 'phone')}),
        ('Quyền hạn', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'city', 'state', 'address', 'phone', 'is_staff', 'is_active'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
