from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import HousingPost, Image

@receiver(post_save, sender=HousingPost)
@receiver(post_delete, sender=HousingPost)
@receiver(post_save, sender=Image)
@receiver(post_delete, sender=Image)
def invalidate_post_cache(sender, instance, **kwargs):
    cache_keys = [
        f'post_detail_{instance.pk}',
        'post_list_map',
    ]
    cache.delete_many(cache_keys)