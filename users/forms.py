from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser, BusinessProfile, ClientProfile

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'profile_picture')
        
class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ('business_name', 'description', 'address', 'city', 'logo')
        
class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ('date_of_birth',)
