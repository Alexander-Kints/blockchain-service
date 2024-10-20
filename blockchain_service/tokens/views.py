import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .serializers import TokenSerializer
from .models import Token
from .web3_service import Web3Service, generate_random_str, is_hex
from .paginations import TokenListAPIViewPagination


class TokenCreateAPIView(APIView):
    def post(self, request):
        model_serializer = TokenSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)

        if not is_hex(request.data['owner']):
            return Response({"message": "no valid owner address"})

        unique_hash = generate_random_str(20)
        model_serializer.save(unique_hash=unique_hash)
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
        if tx_hash != '':
            model_serializer.save(tx_hash=tx_hash)

        return Response(model_serializer.data)


class TokenListAPIView(ListAPIView):
    # Сортировка, чтобы не ругался UnorderedObjectListWarning на пагинацию
    queryset = Token.objects.all().order_by('id')
    serializer_class = TokenSerializer
    pagination_class = TokenListAPIViewPagination


class TokenTotalSupplyAPIView(APIView):
    def get(self, request):
        service = Web3Service(
            network_url=os.environ.get('NFT_NETWORK_URL'),
            contract_address=os.environ.get('NFT_CONTRACT_ADDRESS'),
            abi_filepath='static/ERC_721_abi.json'
        )
        return Response({"result": service.total_supply()})
