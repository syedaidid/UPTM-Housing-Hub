from django.core.cache import cache
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Profile)
def edit_profile(sender, instance, **kwargs):
    cache_keys = [
        f'profile_image_{instance.pk}'
    ]
    # Invalidate cache keys
    cache.delete_many(cache_keys)