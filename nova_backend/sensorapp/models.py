from django.db import models
from django.utils import timezone

class SensorData(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value}"
