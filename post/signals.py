from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import HousingPost

@receiver(post_save)
@receiver(post_delete)
def clear_the_cache(**kwargs):
    cache.clear()

@receiver(post_save, sender=HousingPost)
def delete_post_list_cache(sender, instance, **kwargs):
    # Invalidate cache for the post list map view
    cache_key = 'post_list_map_cache'
    cache.delete(cache_key)
