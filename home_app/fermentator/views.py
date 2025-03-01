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
@csrf_exempt  # Obejít CSRF ochranu pro tento endpoint
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Uložení dat do modelu
            sensor_data = SensorData(
                temperature=data['temperature'],
                humidity=data['humidity'],
                desired_temp=data['desired_temp']
            )
            sensor_data.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid_request'})

# 🔥 Spuštění fermentace
@csrf_exempt  # Obejít CSRF ochranu pro tento endpoint
def start_fermentation(request):
    if request.method == 'POST':
        ferment_name = request.POST.get('name', 'Default Ferment')
        try:
            # Opraveno: použití is_active místo active
            ferment_batch = FermentBatch.objects.create(name=ferment_name, is_active=True)
            return JsonResponse({'status': 'success', 'id': ferment_batch.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid_request'})


@csrf_exempt  # Obejít CSRF ochranu pro tento endpoint
def stop_fermentation(request):
    if request.method == 'POST':
        try:
            # Deaktivace všech fermentací, které jsou aktivní
            FermentBatch.objects.filter(is_active=True).update(is_active=False)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid_request'})



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
