from django.db import models

# Create your models here.



class OneTimePassword(models.Model):
    
    email = models.EmailField()
    
    phone = models.CharField(max_length=12)
    
    username = models.CharField(max_length=13)
    
    user_type = models.CharField(max_length=7)
    
    password = models.CharField(max_length=16)
    
    
    token = models.CharField(
        max_length=250,
        unique=True
    )
    
    code = models.CharField(max_length=6)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "One-Time Password"
        verbose_name_plural = "One-Time Passwords"
        
    
    def __str__(self):
        return f'{self.code}----{self.token}'
