from django.db import models

class Admintable(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.EmailField(unique=True,null=True)
    admin_password=models.CharField(max_length=50,unique=True)