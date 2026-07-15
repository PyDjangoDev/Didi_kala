from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    
    class Meta :
        db_table = 'account'
        verbose_name = 'کاربر'
        verbose_name_plural = "کاربران"  
        
        
