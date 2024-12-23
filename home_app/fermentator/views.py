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
            desired_temp = data.get("desired_temp")  # Můžete mít jako None

            # Pokud není desired_temp zaslána, můžete nastavit na výchozí hodnotu (např. 30)
            if desired_temp is None:
                desired_temp = 30  # nebo nějaká jiná logika, kterou chcete použít

            # Validace hodnot
            if temperature is not None and humidity is not None:
                # Uložení do databáze
                SensorData.objects.create(temperature=temperature, humidity=humidity, desired_temp=desired_temp)
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

            # Získání poslední hodnoty desired_temp
            latest_data = SensorData.objects.last()
            if latest_data:
                latest_data.desired_temp += change
                latest_data.save()
                return JsonResponse({"status": "success", "desired_temp": latest_data.desired_temp}) #TODO toto vrací hodnotu z databáze, tedy vždy 0
            else:
                return JsonResponse({"status": "error", "message": "No data available!"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON!"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method!"}, status=405)

