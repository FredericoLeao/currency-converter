from rest_framework import serializers

class CurrencyConvertSerializer(serializers.Serializer):
    src_currency = serializers.CharField(max_length=5)
    tgt_currency = serializers.CharField(max_length=5)
    amount = serializers.FloatField(max_digits=12)
