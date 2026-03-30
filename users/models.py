from django.db import models

# Create your models here.

class UserRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    phonenumber = models.IntegerField()
    address = models.TextField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    is_active = models.BooleanField(default=False)  

    def __str__(self):
        return self.name