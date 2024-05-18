from django.db import models

from Pump.models import DeliveryBoy, Fuel, Mechanic, Pump
import User

class Newuser(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20)

    
    


class Booking(models.Model):
    user = models.ForeignKey(Newuser, on_delete=models.CASCADE)
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE)
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, null=True, blank=True)
    delivery_boy = models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    mechanic_needed = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=True)
    delivery_boy_contacted = models.BooleanField(default=True)
    


class Complaint(models.Model):
    user = models.ForeignKey(Newuser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField()
