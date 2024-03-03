from datetime import datetime, timezone
import requests
from converter.models import CurrencyValues

EXT_PRICE_API='https://economia.awesomeapi.com.br/json/last'
ACCEPTED_CODES = ['BRL', 'EUR', 'BTC', 'ETH']
CRYPTO_CURRENCIES = ['ETH', 'BTC']
CACHE_TTL = 10 # the time in seconds the currency price cache will be valid


class CurrencyConvertService:

    def store_cache(self, currency_code, usd_price):
        currency_cache = CurrencyValues()
        currency_cache.currency_code = currency_code
        currency_cache.price_in_usd = usd_price
        currency_cache.save()

    def get_usd_price_from_cache(self, currency_code) -> float:
        res_local = CurrencyValues.objects.filter(
            currency_code__exact=currency_code).first()
        if not res_local:
            return -1
        delta = datetime.now(timezone.utc) - res_local.updated_at
        if delta.seconds > CACHE_TTL:
            return -2
        return res_local.price_in_usd

    def get_usd_price(self, currency_code) -> float:
        currency_code = currency_code.upper()
        if currency_code == 'USD':
            return 1
        if currency_code not in ACCEPTED_CODES:
            return -1

        usd_price_from_cache = self.get_usd_price_from_cache(currency_code)
        if usd_price_from_cache >= 0:
            return usd_price_from_cache

        res = requests.get(f'{EXT_PRICE_API}/{currency_code}-USD', timeout=6)
        if res.status_code == 200:
            usd_price = res.json()[f'{currency_code}USD']['bid']
            self.store_cache(currency_code, usd_price)
            return usd_price

        return -2

    def convert(self, data) -> float:
        src_usd_price = self.get_usd_price(data['src_currency'])
        tgt_usd_price = self.get_usd_price(data['tgt_currency'])
        if float(src_usd_price) < 0 or float(tgt_usd_price) < 0:
            return -1
        converted_value = ((float(src_usd_price) * float(data['amount'])) *
                           (1 / float(tgt_usd_price)))
        return converted_value
