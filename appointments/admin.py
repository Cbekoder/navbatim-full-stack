from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'business', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('client__username', 'business__business_name', 'service__name')
    date_hierarchy = 'date'
