from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Navbatim.uz")
    site_description = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
    class Meta:
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"
