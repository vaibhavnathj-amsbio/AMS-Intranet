from django.contrib import admin
from .models import Currencies, MasterCurrencies, DataOwners, NwResearchAreaIds

admin.site.register(Currencies)
admin.site.register(MasterCurrencies)
admin.site.register(DataOwners)
admin.site.register(NwResearchAreaIds)