from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('FedexUK',views.fedex, name='fedex' ),
    path('FedexUSA',views.fedex, name='fedex' ),
    path('DHL',views.dhl, name='dhl' ),
    path('loadtable_UK',views.loadCSVtoHTML, name='loadtable_UK'),
    path('loadtable_USA',views.loadCSVtoHTML, name='loadtable_USA'),
]
