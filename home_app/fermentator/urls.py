# your_app_name/urls.py
from django.urls import path
from .views import home, receive_data

urlpatterns = [
    path('', home, name='home'),  # domovská stránka
    path('api/data/', receive_data, name='receive_data'),

]
