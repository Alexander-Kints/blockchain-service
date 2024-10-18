from rest_framework import serializers

from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    unique_hash = serializers.CharField(required=False)
    tx_hash = serializers.CharField(required=False)

    class Meta:
        model = Token
        fields = '__all__'
