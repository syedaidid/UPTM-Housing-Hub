from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class HousingPost(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    FURNISHED_CHOICES = [
        ('fully furnished', 'Fully Furnished'),
        ('partially furnished', 'Partially Furnished'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(default=None)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None)
    number_of_people = models.IntegerField(default=1)  # Assuming it's a positive integer
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    utilities_included = models.BooleanField(default=False)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Decimal field for monthly payment amount
    furnished_type = models.CharField(max_length=20, choices=FURNISHED_CHOICES, default=None)
    furnished = models.TextField(default=None)
    facilities = models.TextField(default=None)
    accessibilities = models.TextField(default=None)
    address = models.CharField(max_length=200, null=True)
    verified = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='housing_posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    

class Image(models.Model):
    image = models.ImageField(upload_to='image_post')
    housing_post = models.ForeignKey(HousingPost, on_delete=models.CASCADE, related_name='images', default=None)

    def __str__(self):
        return self.image.url