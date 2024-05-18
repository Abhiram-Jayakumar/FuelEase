from django.db import models

from Pump.models import DeliveryBoy

# Create your models here.
class DeliveryBoyComplaint(models.Model):
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)