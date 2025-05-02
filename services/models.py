from django.db import models
from django.urls import reverse
from users.models import BusinessProfile, CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, help_text="Icon name from the icon set")
    icon_color = models.CharField(max_length=50, default="bg-emerald-100 text-emerald-500")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


# Now that Category is defined, we can update BusinessProfile to include the categories field
# This needs to be done here to avoid circular imports
BusinessProfile.categories = models.ManyToManyField(Category, related_name='businesses', blank=True)


class Service(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    has_discount = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.business.business_name}"


class BusinessHours(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='business_hours')
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Business Hours"
        ordering = ['day']
        unique_together = ['business', 'day']

    def __str__(self):
        if self.is_closed:
            return f"{self.business.business_name} - {self.get_day_display()} - Closed"
        return f"{self.business.business_name} - {self.get_day_display()} - {self.opening_time} to {self.closing_time}"


class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.rating}"


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorites')
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'business']

    def __str__(self):
        return f"{self.user.username} - {self.business.business_name}"


class Deal(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='deals')
    title = models.CharField(max_length=200)
    description = models.TextField()
    discount_percentage = models.PositiveIntegerField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='deals/', blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.business.business_name}"
