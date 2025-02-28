from .models import FermentBatch, SensorData


def save_sensor_data(temperature, humidity, desired_temp):
    active_batch = FermentBatch.objects.filter(is_active=True).first()  # Najde aktivní fermentaci

    SensorData.objects.create(
        temperature=temperature,
        humidity=humidity,
        desired_temp=desired_temp,
        ferment_batch=active_batch  # Může být None, pokud není aktivní fermentace
    )


def start_new_ferment(name):
    # Deaktivujeme všechny ostatní fermentace
    FermentBatch.objects.filter(is_active=True).update(is_active=False)

    # Vytvoříme novou fermentaci a nastavíme jako aktivní
    new_batch = FermentBatch.objects.create(name=name, is_active=True)

    return new_batch


def stop_fermentation():
    FermentBatch.objects.filter(is_active=True).update(is_active=False)
