from django.urls import path
from .views import *

app_name = 'business'

urlpatterns = [
    # Dashboard
    path('dashboard/', business_dashboard, name='business_dashboard'),

    # Services management
    path('services/', business_services, name='business_services'),
    path('services/add/', add_service, name='add_service'),
    path('services/edit/<int:service_id>/', edit_service, name='edit_service'),
    path('services/delete/<int:service_id>/', delete_service, name='delete_service'),
    path('services/toggle/<int:service_id>/', toggle_service_status, name='toggle_service_status'),

    # Appointments management
    path('appointments/', business_appointments, name='business_appointments'),
    path('appointments/update/<int:appointment_id>/', update_appointment_status,
         name='update_appointment_status'),
    # path('appointments/<int:appointment_id>/details/', appointment_details, name='appointment_details'),
    # path('appointments/note/', add_appointment_note, name='add_appointment_note'),
    #
    # # Profile management
    # path('profile/edit/', edit_business_profile, name='edit_business_profile'),
    #
    # # Analytics
    # path('analytics/', business_analytics, name='business_analytics'),
    #
    # # Reviews
    # path('reviews/', business_reviews, name='business_reviews'),

    # # Client management
    # path('clients/', business_clients, name='clients'),
    # path('clients/<int:client_id>/', client_detail, name='client_detail'),
    # path('clients/<int:client_id>/appointments/', client_appointments, name='client_appointments'),
    # path('clients/note/add/', add_client_note, name='add_client_note'),
    # path('clients/note/delete/', delete_client_note, name='delete_client_note'),
    # path('clients/block/', block_client, name='block_client'),
    # path('clients/<int:client_id>/unblock/', unblock_client, name='unblock_client'),
    # path('clients/export/', export_clients, name='export_clients'),
]
