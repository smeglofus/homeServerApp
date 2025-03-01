# your_app_name/urls.py
from django.urls import path
from .views import home, receive_data, start_fermentation, stop_fermentation, update_temp, get_sensor_data

urlpatterns = [
    path('', home, name='home'),
    path('api/data/', receive_data, name='receive_data'),
    path('get_sensor_data/', get_sensor_data, name='get_sensor_data'),  # Zkontroluj, zda je tato řádka přítomná
    path('start_fermentation/', start_fermentation, name='start_fermentation'),
    path('stop_fermentation/', stop_fermentation, name='stop_fermentation'),
    path('update_temp/', update_temp, name='update_temp'),
]

