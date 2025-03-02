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

    # Získání všech fermentací
    ferment_batches = FermentBatch.objects.all()  # ZDE ZMĚNA

    return render(request, 'home.html', {
        'data': data,
        'active_ferment': active_ferment,
        'ferment_batches': ferment_batches  # PŘIDÁNO DO KONTEXTU
    })



# 📌 API pro příjem dat ze senzoru
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Získání aktivní fermentační várky
            active_batch = FermentBatch.objects.filter(is_active=True).first()
            if not active_batch:
                return JsonResponse({'status': 'error', 'message': 'No active fermentation batch found!'})

            # Uložení dat s napojením na aktivní várku
            sensor_data = SensorData.objects.create(
                temperature=data['temperature'],
                humidity=data['humidity'],
                desired_temp=data['desired_temp'],
                ferment_batch=active_batch
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid_request'})


# 🔥 Spuštění fermentace
@csrf_exempt
def start_fermentation(request):
    if request.method == 'POST':
        try:
            # Získání jména fermentace - z FormData nebo JSON
            ferment_name = request.POST.get('name')  # FormData

            # Fallback pro JSON, pokud přijde JSON request
            if not ferment_name:
                data = json.loads(request.body)
                ferment_name = data.get('name', 'Default Ferment')

            ferment_batch = FermentBatch.objects.create(name=ferment_name, is_active=True)
            return JsonResponse({'status': 'success', 'id': ferment_batch.id, 'name': ferment_batch.name})
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



def get_batch_data(request, batch_id):
    try:
        batch_data = FermentBatch.objects.get(id=batch_id)
    except FermentBatch.DoesNotExist:
        return JsonResponse({'error': 'Fermentační várka neexistuje'}, status=404)

    # Získání souvisejících senzorových dat
    sensor_data = batch_data.sensor_data.all()
    print(sensor_data)  # Debugging output

    # Pokud nejsou žádná data, vrátíme prázdný JSON
    if not sensor_data.exists():
        return JsonResponse({'labels': [], 'temperature': [], 'humidity': []})

    # Připravíme data pro JSON odpověď
    data = {
        'labels': [datum.timestamp.isoformat() for datum in sensor_data],
        'temperature': [datum.temperature for datum in sensor_data],
        'humidity': [datum.humidity for datum in sensor_data],
    }

    return JsonResponse(data)

@csrf_exempt  # Obejít CSRF ochranu pro tento endpoint
def delete_batch(request, batch_id):
    if request.method == 'POST':
        try:
            batch = FermentBatch.objects.get(id=batch_id)
            batch.delete()  # Smazání várky
            return JsonResponse({'status': 'success'})
        except FermentBatch.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Várka neexistuje'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid_request'}, status=400)
