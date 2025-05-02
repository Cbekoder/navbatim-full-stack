from django.urls import path
from . import views

app_name = 'services'  # Add namespace to avoid URL name conflicts

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('business/<int:pk>/', views.business_detail, name='business_detail'),
    path('add-favorite/<int:business_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:business_id>/', views.remove_favorite, name='remove_favorite'),
    path('add-review/<int:business_id>/', views.add_review, name='add_review'),
    path('deals/', views.deals_list, name='deals_list'),
    path('map/', views.map_view, name='map_view'),
]
