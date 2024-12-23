from django.db import models

class SensorData(models.Model):
    temperature = models.FloatField(default=155.0)
    humidity = models.FloatField(default=155.0)
    desired_temp = models.FloatField(default=155.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temperature: {self.temperature}, Humidity: {self.humidity}, Desired temperature: {self.desired_temp}"
