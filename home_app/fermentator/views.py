from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData

# Create your views here.
def home(request):
    data = SensorData.objects.all().order_by('-timestamp')  # Data seřazená podle času #
    return render(request, 'home.html', {'data': data})

@csrf_exempt
def receive_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Debug

            temperature = data.get("temperature")
            humidity = data.get("humidity")
            desired_temp = data.get("desired_temp")

            if desired_temp is None:
                desired_temp = 30

            if temperature is not None and humidity is not None:
                SensorData.objects.create(temperature=temperature, humidity=humidity, desired_temp=desired_temp)
                print("Database data:", SensorData.objects.all().values())  # Debug databáze
                return JsonResponse({"status": "success", "message": "Data saved successfully!", "desired_temp": desired_temp})
            else:
                return JsonResponse({"status": "error", "message": "Invalid data!"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method!"}, status=405)


@csrf_exempt
def update_temp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            change = data.get("change", 0)
            print("Received change request:", change)

            latest_data = SensorData.objects.last()
            if latest_data:
                print("Latest database entry before update:", latest_data)
                latest_data.desired_temp += change
                latest_data.save()
                print("Updated desired_temp:", latest_data.desired_temp)

                return JsonResponse({"status": "success", "desired_temp": latest_data.desired_temp})
            else:
                return JsonResponse({"status": "error", "message": "No data available!"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method!"}, status=405)


def get_sensor_data(request):
    data = SensorData.objects.order_by('-timestamp')[:50]  # Posledních 50 záznamů
    response_data = {
        "labels": [entry.timestamp.strftime("%H:%M:%S") for entry in data],
        "temperature": [entry.temperature for entry in data],
        "humidity": [entry.humidity for entry in data],
    }
    return JsonResponse(response_data)