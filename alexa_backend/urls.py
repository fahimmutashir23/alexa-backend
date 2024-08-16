from .views import alexa_api_view
from django.urls import path

urlpatterns = [
    path('voice/', alexa_api_view, name='alexa_backend'),
]
