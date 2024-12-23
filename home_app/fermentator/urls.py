# your_app_name/urls.py
from django.urls import path
from .views import home, receive_data, update_temp

urlpatterns = [
    path('', home, name='home'),  # domovská stránka
    path('api/data/', receive_data, name='receive_data'),
    path('api/update_temp/', update_temp, name='update_temp'),
]
