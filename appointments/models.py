import requests
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from services.models import Service, BusinessProfile

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments')
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.client.username} - {self.business.business_name} - {self.date} {self.time}"
    
    @property
    def is_past(self):
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return appointment_datetime < timezone.now()

    def save(self, *args, **kwargs):
        try:
            url = f"https://api.telegram.org/bot8100931705:AAFANyw18iwh0Ro41hN5yXM_5-HuHCGMFWU/sendMessage"
            payload = {
                "chat_id": 5729115581,
                "text": f"📅 Yangi navbat qo'shildi!\n"
                    f"👤 Mijoz: {self.client.get_full_name() or self.client.username}\n"
                    f"🏢 Biznes: {self.business.business_name}\n"
                    f"💼 Xizmat: {self.service.name}\n"
                    f"📆 Sana: {self.date}\n"
                    f"⏰ Vaqt: {self.time}\n"
                    f"📌 Holat: {self.get_status_display()}"
            }
            response = requests.post(url, json=payload)
            if response.status_code == 200 and response.json().get("ok"):
                print("Message sent successfully!")
            else:
                print(f"Error sending message: {response.json()}")
        except Exception as e:
            print(f"Error: {e}")
        super().save(*args, **kwargs)
