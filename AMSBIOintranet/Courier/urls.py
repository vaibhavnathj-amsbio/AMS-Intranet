from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('fedex',views.fedex, name='fedex' ),
    path('dhl',views.dhl, name='dhl' ),
]
