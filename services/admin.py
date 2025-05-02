from django.contrib import admin
from .models import Category, Service, BusinessHours, Review, Favorite, Deal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'business', 'category', 'price', 'duration', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'business__business_name')


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('business', 'day', 'opening_time', 'closing_time', 'is_closed')
    list_filter = ('day', 'is_closed')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('business', 'user', 'rating', 'created_at')
    list_filter = ('rating',)

    def business(self, obj):
        return obj.business

    business.short_description = 'Business'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'business', 'created_at')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'business', 'discount_percentage', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'discount_percentage')
    search_fields = ('title', 'business__business_name')
