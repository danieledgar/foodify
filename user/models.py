from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,max_length=50, blank=True, null=True)
    phone_number = models.IntegerField(unique=True,blank=True, null=True)

    def __str__(self):
        return self.email


