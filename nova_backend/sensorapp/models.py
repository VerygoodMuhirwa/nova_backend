from djongo import models
from django.utils import timezone

class SensorData(models.Model):
    user = models.CharField(max_length=100)
    sensorName = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    physicalQuantity = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sensor: {self.sensorName} | Value: {self.value} | Timestamp: {self.timestamp}"
