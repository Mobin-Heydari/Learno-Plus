from django.db import models
from django.utils import timezone




class OneTimePassword(models.Model):
    # Define the possible statuses for the OTP
    class OtpStatus(models.TextChoices):
        ACTIVE = 'ACT', 'Active'     # OTP is currently active
        EXPIRED = 'EXP', 'Expired'   # OTP has expired

    # Field to store the status of the OTP
    status = models.CharField(
        max_length=3,
        choices=OtpStatus.choices,
        default=OtpStatus.ACTIVE  # Default status is 'Active'
    )

    email = models.EmailField()  # Field to store the user's email address
    phone = models.CharField(max_length=12)  # Field to store the user's phone number
    username = models.CharField(max_length=13)  # Field to store the user's username
    user_type = models.CharField(max_length=7)  # Field to store the type of user
    password = models.CharField(max_length=16)  # Field to store the user's password

    # Field to store a unique token for the OTP
    token = models.CharField(max_length=250, unique=True)
    
    code = models.CharField(max_length=6)  # Field to store the OTP code
    created = models.DateTimeField(auto_now_add=True)  # Timestamp when the OTP is created
    updated = models.DateTimeField(auto_now=True)  # Timestamp when the OTP is last updated

    # Field to store the expiration date and time of the OTP
    expiration_date_time = models.DateTimeField(blank=True, null=True,)

    class Meta:
        verbose_name = "One-Time Password"  # Human-readable name for the model
        verbose_name_plural = "One-Time Passwords"  # Human-readable plural name for the model

    # String representation of the model instance
    def __str__(self):
        return f'{self.code}----{self.token}'

    # Method to calculate and set the expiration time for the OTP
    def get_expiration(self):
        created = self.created  # Get the creation time of the OTP
        expiration = created + timezone.timedelta(minutes=1)  # Set expiration to 1 minute after creation
        self.expiration_date_time = expiration  # Assign the calculated expiration time to the instance
        self.save()  # Save the changes to the database

    # Method to validate the status of the OTP based on its expiration time
    def status_validation(self):
        if self.expiration_date_time <= timezone.now():  # Check if the current time is past the expiration time
            self.status = 'EXP'  # Update the status to 'Expired'
            return self.status  # Return the updated status
        else:
            return self.status  # Return the current status if not expired