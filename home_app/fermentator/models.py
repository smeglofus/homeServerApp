from django.db import models

class FermentBatch(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)  # Jen jeden může být aktivní
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Active: {self.is_active})"

class SensorData(models.Model):
    temperature = models.FloatField(default=155.0)
    humidity = models.FloatField(default=155.0)
    desired_temp = models.FloatField(default=155.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    ferment_batch = models.ForeignKey(
        FermentBatch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True  # Pokud není aktivní proces, může být NULL
    )

    def __str__(self):
        return f"Temp: {self.temperature}, Humidity: {self.humidity}, Batch: {self.ferment_batch}"
