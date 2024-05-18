from django.db import models

from Pump.models import Mechanic

# Create your models here.
class MechanicComplaint(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    admin_reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)