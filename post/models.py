from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class HousingPost(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None)
    number_of_people = models.IntegerField(default=1)  # Assuming it's a positive integer
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Decimal field for monthly payment amount
    furnished = models.TextField(default=None)
    facilities = models.TextField(default=None)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='housing_posts')