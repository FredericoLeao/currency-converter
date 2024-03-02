
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from .serializers import CurrencyConvertSerializer
from .services import CurrencyConvertService

class CurrencyConvertAPIView(APIView):
    def get(self, request, **kwargs):
        data_serialized = CurrencyConvertSerializer(data=kwargs)
        data_serialized.is_valid(raise_exception=True)
        converter_service = CurrencyConvertService()
        convert_result = converter_service.convert(data_serialized.data)
        return Response(data=convert_result, status=HTTP_200_OK)
