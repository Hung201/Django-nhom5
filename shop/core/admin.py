from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    def user_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return "No Image"

    user_image.short_description = 'Profile Image'  # Đổi tên cột trong Admin

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'image')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'city', 'state', 'address', 'phone')}),
        ('Quyền hạn', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image', 'city', 'state', 'address', 'phone', 'is_staff', 'is_active'),
        }),
    )

    list_display = ('username', 'email', 'user_image', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
