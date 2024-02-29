
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .serializers import CurrencyConvertSerializer

class CurrencyConvertAPIView(APIView):
    def get(self, request, **kwargs):
        data_serialized = CurrencyConvertSerializer(data=kwargs)
        data_serialized.is_valid(raise_exception=True)
        # TODO: Run convertion
        return Response(data={}, status=HTTP_200_OK)
