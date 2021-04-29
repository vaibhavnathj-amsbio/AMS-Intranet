from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('fedexUK',views.fedex, name='fedexUK' ),
    path('fedexUSA',views.fedex, name='fedexUSA' ),
]
