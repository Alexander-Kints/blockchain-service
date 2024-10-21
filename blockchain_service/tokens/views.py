import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from .serializers import TokenSerializer
from .models import Token
from .web3_service import Web3Service, generate_random_str, is_hex
from .paginations import TokenListAPIViewPagination


class TokenCreateAPIView(APIView):
    @extend_schema(
        description='Mint Token',
        request=inline_serializer(
            name='TokenRequestBody',
            fields={
                'media_url': serializers.CharField(),
                'owner': serializers.CharField(default='hex_string')
            }
        ),
        responses={
            200: TokenSerializer,
            400: inline_serializer(
                name='BadRequest',
                fields={
                    'message': serializers.CharField(
                        default='no valid owner address'
                    )
                }
            )
        }
    )
    def post(self, request):
        model_serializer = TokenSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)

        if not is_hex(request.data['owner']):
            return Response(
                {"message": "no valid owner address"},
                status=400
            )

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
    @extend_schema(
        description='Get total supply of Token',
        responses={
            200: inline_serializer(
                name='TotalSupplyResponse',
                fields={
                    'result': serializers.IntegerField(default=10000)
                }
            )
        }
    )
    def get(self, request):
        service = Web3Service(
            network_url=os.environ.get('NFT_NETWORK_URL'),
            contract_address=os.environ.get('NFT_CONTRACT_ADDRESS'),
            abi_filepath='static/ERC_721_abi.json'
        )
        return Response({"result": service.total_supply()})
