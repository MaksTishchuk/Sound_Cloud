from rest_framework import serializers


class GoogleAuthSerializer(serializers.Serializer):
    """Сериализация данных от Google"""

    email = serializers.EmailField()
    token = serializers.CharField()
