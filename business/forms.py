from django import forms
from django.forms import inlineformset_factory
from users.models import BusinessProfile
from services.models import Service, BusinessHours

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'category', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'min': 0, 'step': 1000}),
            'duration': forms.NumberInput(attrs={'min': 5, 'step': 5}),
        }

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['business_name', 'description', 'phone_number', 'address',
                  'city', 'website', 'logo', 'cover_image']
        # Removed 'categories', 'latitude', 'longitude' as they might be causing issues
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class BusinessHoursForm(forms.ModelForm):
    class Meta:
        model = BusinessHours
        fields = ['day', 'opening_time', 'closing_time', 'is_closed']
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
        }

# Create an inline formset for BusinessHours
BusinessHoursFormSet = inlineformset_factory(
    BusinessProfile,
    BusinessHours,
    form=BusinessHoursForm,
    extra=7,  # One form for each day of the week
    max_num=7,
    can_delete=False,
)
