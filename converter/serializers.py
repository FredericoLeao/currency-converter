from rest_framework import serializers

class CurrencyConvertSerializer(serializers.Serializer):
    src_currency = serializers.CharField(max_length=5)
    tgt_currency = serializers.CharField(max_length=5)
    amount = serializers.DecimalField(max_digits=12, decimal_places=4)
