from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData, FermentBatch
from .utils import save_sensor_data, start_new_ferment, stop_fermentation

# 🌍 Hlavní stránka
def home(request):
    data = SensorData.objects.all().order_by('-timestamp')
    active_ferment = FermentBatch.objects.filter(is_active=True).first()
    return render(request, 'home.html', {'data': data, 'active_ferment': active_ferment})

# 📌 API pro příjem dat ze senzoru
@csrf_exempt
def receive_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            temperature = data.get("temperature")
            humidity = data.get("humidity")
            desired_temp = data.get("desired_temp", 30)  # Defaultní hodnota

            if temperature is not None and humidity is not None:
                save_sensor_data(temperature, humidity, desired_temp)
                return JsonResponse({"status": "success", "message": "Data saved successfully!", "desired_temp": desired_temp})
            else:
                return JsonResponse({"status": "error", "message": "Invalid data!"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method!"}, status=405)

# 🔥 Spuštění fermentace
@csrf_exempt
def start_fermentation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            ferment_name = data.get("name")

            if not ferment_name:
                return JsonResponse({"status": "error", "message": "Musíte zadat název fermentace!"}, status=400)

            # Vytvoří novou aktivní fermentaci
            ferment_batch = FermentBatch.objects.create(name=ferment_name, active=True)

            return JsonResponse(
                {"status": "success", "message": f"Fermentace '{ferment_name}' byla spuštěna!", "id": ferment_batch.id})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Chybný formát JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Neplatná metoda požadavku!"}, status=405)


@csrf_exempt
def stop_fermentation(request):
    if request.method == "POST":
        FermentBatch.objects.filter(active=True).update(active=False)
        return JsonResponse({"status": "success", "message": "Všechny fermentace byly zastaveny!"})

    return JsonResponse({"status": "error", "message": "Neplatná metoda požadavku!"}, status=405)


# 🔄 Aktualizace požadované teploty aktivní fermentace
@csrf_exempt
def update_temp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            change = data.get("change", 0)

            active_batch = FermentBatch.objects.filter(is_active=True).first()
            if active_batch:
                latest_data = SensorData.objects.filter(ferment_batch=active_batch).last()
                if latest_data:
                    latest_data.desired_temp += change
                    latest_data.save()
                    return JsonResponse({"status": "success", "desired_temp": latest_data.desired_temp})

            return JsonResponse({"status": "error", "message": "No active fermentation or sensor data!"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method!"}, status=405)

# 📊 Získání posledních senzorových dat
def get_sensor_data(request):
    data = SensorData.objects.order_by('-timestamp')[:50]
    response_data = {
        "labels": [entry.timestamp.strftime("%H:%M:%S") for entry in data],
        "temperature": [entry.temperature for entry in data],
        "humidity": [entry.humidity for entry in data],
    }
    return JsonResponse(response_data)
