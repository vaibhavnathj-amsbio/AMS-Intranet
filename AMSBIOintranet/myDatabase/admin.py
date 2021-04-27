from django.contrib import admin
from .models import Currencies, MasterCurrencies


# The following models are available in admin panel.
admin.site.register(Currencies)
admin.site.register(MasterCurrencies)