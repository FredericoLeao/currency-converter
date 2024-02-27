from django.db import models

class TimestampedModel(models.Model):
    ''' timestamped model to be extended by other models '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CurrencyValues(TimestampedModel):
    ''' store currency values '''
    currency_code = models.CharField(max_length=5)
    price_in_usd = models.DecimalField(max_digits=12, decimal_places=4)

class Config(TimestampedModel):
    ''' general configuration store '''
    attribute = models.CharField(max_length=50)
    value = models.CharField(max_length=256)
