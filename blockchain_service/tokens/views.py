from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import TokenSerializer
from .models import Token


class TokenCreateAPIView(APIView):
    def post(self, request):
        model_serializer = TokenSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save(unique_hash="testhash123", tx_hash="terterg")
        print(model_serializer.data)
        return Response(model_serializer.data)


class TokenListAPIView(ListAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
