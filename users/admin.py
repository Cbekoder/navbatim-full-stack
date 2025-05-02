from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, BusinessProfile, ClientProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'user_type', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_picture')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BusinessProfile)
admin.site.register(ClientProfile)
