from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('FedexUK',views.fedex, name='fedex' ),
    path('FedexUSA',views.fedex, name='fedex' ),
    path('DHL',views.dhl, name='dhl' ),
    path('loadtable',views.loadCSVtoHTML, name='loadtable'),
]
