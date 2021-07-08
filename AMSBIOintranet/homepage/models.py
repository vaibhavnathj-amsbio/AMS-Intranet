from django.db import models


class liveCurrencyRate(models.Model):
    base_currency = models.CharField(max_length=64, blank=True, null=True, verbose_name='FROM')
    to_currency = models.CharField(max_length=64, blank=True, null=True, verbose_name='TO')
    live_rate = models.FloatField(verbose_name='Live Rate', blank=True, null=True)

    def __str__(self):
        return self.base_currency + '/' + self.to_currency + ': ' + str(self.live_rate)
 

    class Meta:
        verbose_name_plural = 'Live Rate'
        app_label = 'homepage'