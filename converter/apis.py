
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from .serializers import CurrencyConvertSerializer
from .services import CurrencyConvertService

class CurrencyConvertAPIView(APIView):
    def get(self, request, **kwargs):
        data_serialized = CurrencyConvertSerializer(data=kwargs)
        if not data_serialized.is_valid():
            return Response(data=data_serialized.errors,
                            status=HTTP_403_FORBIDDEN)
        converter_service = CurrencyConvertService()
        convert_result = converter_service.convert(data_serialized.data)
        return Response(data={'converted_amount': convert_result},
                        status=HTTP_200_OK)
