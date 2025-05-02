from django import forms
from django.core.mail import send_mail
from django.conf import settings

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    
    def save(self):
        # This would typically send an email
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        full_message = f"Message from {name} ({email}):\n\n{message}"
        
        # In a real application, you would send an email here
        # send_mail(subject, full_message, email, [settings.DEFAULT_FROM_EMAIL])
        
        # For now, we'll just print to console
        print(f"Contact form submission: {subject}")
        print(full_message)
