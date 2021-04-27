from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('fedexUK',views.fedexUK, name='fedexUK' ),
    path('fedexUSA',views.fedexUSA, name='fedexUSA' ),
]
