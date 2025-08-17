from django.urls import path
from . import views

urlpatterns = [
    path("webhook", views.whatsapp_webhook, name='whatsapp_webhook'),
    path("property", views.property_list, name='property_list'),
    path("media/<str:media_id>/", views.fetch_media, name="fetch_media")
]