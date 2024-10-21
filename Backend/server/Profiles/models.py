from django.db import models
from Users.models  import User


class UserProfile(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, 
        related_name="user_profile"
    )
    
    bio = models.TextField(
        max_length=500, 
        blank=True,
        null=True
    )
    
    image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    full_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}.....{self.full_name}"


    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles" 
