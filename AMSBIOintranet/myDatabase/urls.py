from django.urls import path
from . import views

urlpatterns = [
    path('index',views.index, name = 'index'),
    path('AddNewSupplier', views.addNewSupplier, name='AddNewSupplier'),
    path('EditSingleProduct', views.editSingleProduct, name='EditSingleProduct'),
    path('CurrencyValues', views.currencyValue, name='CurrencyValues'),
    path('Search', views.search, name='Search'),
    path('techrecords',views.techRecords, name = 'techrecords'),
]
