from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('',include('homepage.urls')),
    path('myDatabase/',include('myDatabase.urls')),
    path('Courier/',include('Courier.urls')),
    path('admin/', admin.site.urls),
]
