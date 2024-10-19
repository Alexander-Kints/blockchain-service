import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import TokenSerializer
from .models import Token
from .web3_service import Web3Service, generate_random_str


class TokenCreateAPIView(APIView):
    def post(self, request):
        model_serializer = TokenSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)
        unique_hash = generate_random_str(20)
        service = Web3Service(
            network_url=os.environ.get('NFT_NETWORK_URL'),
            contract_address=os.environ.get('NFT_CONTRACT_ADDRESS'),
            abi_filepath='static/ERC_721_abi.json'
        )
        tx_hash = service.create_token(
            media_url=request.data['media_url'],
            unique_hash=unique_hash,
            owner=request.data['owner'],
            private_key=os.environ.get('NFT_PRIVATE_KEY')
        )
        model_serializer.save(unique_hash=unique_hash, tx_hash=tx_hash)
        return Response(model_serializer.data)


class TokenListAPIViewPagination(PageNumberPagination):
    page_size = 200
    max_page_size = 500
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class TokenListAPIView(ListAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    pagination_class = TokenListAPIViewPagination
