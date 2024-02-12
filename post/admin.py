from django.contrib import admin
from .models import HousingPost

@admin.register(HousingPost)
class HousingPostAdmin(admin.ModelAdmin):
    pass
