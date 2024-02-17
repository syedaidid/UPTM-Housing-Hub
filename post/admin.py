from django.contrib import admin
from .models import HousingPost, Image

@admin.register(HousingPost)
class HousingPostAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class Image(admin.ModelAdmin):
    pass