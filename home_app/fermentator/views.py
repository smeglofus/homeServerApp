from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SensorData

# Create your views here.
def home(request):
    data = SensorData.objects.all().order_by('-timestamp')  # Data seřazená podle času
    return render(request, 'home.html', {'data': data})

@csrf_exempt  # Dočasně vypněte CSRF ochranu pro testování
def receive_data(request):
    if request.method == "POST":
        try:
            # Načtení JSON dat z požadavku
            data = json.loads(request.body)

            # Získání hodnot teploty a vlhkosti
            temperature = data.get("temperature")
            humidity = data.get("humidity")

            # Validace hodnot
            if temperature is not None and humidity is not None:
                # Uložení do databáze
                SensorData.objects.create(temperature=temperature, humidity=humidity)
                return JsonResponse({"status": "success", "message": "Data saved successfully!"})
            else:
                return JsonResponse({"status": "error", "message": "Invalid data!"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method!"}, status=405)


