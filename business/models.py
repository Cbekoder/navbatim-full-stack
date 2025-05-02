# from django.db import models
# from django.conf import settings
# from users.models import CustomUser
#
#
# class ClientNote(models.Model):
#     """Notes that business owners can add about clients"""
#     client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='business_notes')
#     business = models.ForeignKey('users.BusinessProfile', on_delete=models.CASCADE, related_name='client_notes')
#     text = models.TextField()
#     created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_notes')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"Note about {self.client.username} by {self.business.business_name}"
#
#
# class BlockedClient(models.Model):
#     """Clients blocked by businesses"""
#     client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocked_by')
#     business = models.ForeignKey('users.BusinessProfile', on_delete=models.CASCADE, related_name='blocked_clients')
#     reason = models.TextField()
#     blocked_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         unique_together = ['client', 'business']
#
#     def __str__(self):
#         return f"{self.client.username} blocked by {self.business.business_name}"
#
#
# class AppointmentNote(models.Model):
#     """Notes that business owners can add to appointments"""
#     appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE, related_name='notes')
#     text = models.TextField()
#     created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='appointment_notes')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"Note for appointment #{self.appointment.id}"
