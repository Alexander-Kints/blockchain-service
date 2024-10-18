from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TokenSerializer


class CreateAPIView(APIView):
    def post(self, request):
        model_serializer = TokenSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save(unique_hash="testhash", tx_hash="hshfhsdf")
        print(model_serializer.data)
        return Response(model_serializer.data)
