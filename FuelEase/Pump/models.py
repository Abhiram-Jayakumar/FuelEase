from django.db import models

class Pump(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    gst_no = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    vstatus=models.IntegerField(default=0)

class Fuel(models.Model):
    pumpId = models.ForeignKey(Pump, on_delete=models.CASCADE)
    fuel_type = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    pumpId = models.ForeignKey(Pump, on_delete=models.CASCADE)
    status = models.BooleanField(default=False) 
 

class DeliveryBoy(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    license_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    pumpId = models.ForeignKey(Pump, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  

class PumpComplaint(models.Model):
    pump = models.ForeignKey(Pump, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)