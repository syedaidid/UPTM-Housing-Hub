from django.db import models
import json

class HousingPost(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    furnished = models.TextField(default=None)
    facilities = models.TextField(default=None)

    def set_facilities(self, facilities):
        self.facilities = json.dumps(facilities)

    def get_facilities(self):
        return json.loads(self.facilities)
