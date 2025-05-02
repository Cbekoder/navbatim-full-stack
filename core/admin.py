from django.contrib import admin
from .models import SiteSettings, Testimonial

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSettings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'is_active', 'created_at')
    list_filter = ('rating', 'is_active')
