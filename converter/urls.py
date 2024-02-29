from django.urls import path

from converter.apis import CurrencyConvertAPIView

urlpatterns = [
    path('convert/<str:src_currency>/<str:tgt_currency>/<str:amount>/',
         CurrencyConvertAPIView.as_view(),
         name='currency-convert'),
]
