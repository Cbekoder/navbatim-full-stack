from django import forms
from django.utils import timezone
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any special requests or notes?'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("You cannot book an appointment in the past.")
        return date
