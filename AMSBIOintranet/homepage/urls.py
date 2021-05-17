from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shipment_details',views.shipmentDetails, name='shipment_details'),
]
