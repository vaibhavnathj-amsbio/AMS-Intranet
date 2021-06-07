from os import name
from django.urls import path
from . import views


# all the eligle urls intranet can handle for myDatabase app
urlpatterns = [
    path('index',views.index, name = 'index'),
    path('AddNewSupplier', views.addNewSupplier, name='AddNewSupplier'),
    path('EditSingleProduct', views.editSingleProduct, name='EditSingleProduct'),
    path('CurrencyValues', views.currencyValue, name='CurrencyValues'),
    path('Search', views.search, name='Search'),
    path('techrecords',views.techRecords, name = 'techrecords'), # used for ajax call
    path('formsubmit',views.FormSubmit, name = 'formsubmit'), # used for ajax call
    path('similarProducts/<str:pk>/',views.similarProducts, name= 'similarProducts'),
]
