from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    """Сериализация данных пользователя"""

    class Meta:
        model = models.AuthUser
        fields = ['avatar', 'country', 'city', 'bio', 'display_name']


class GoogleAuthSerializer(serializers.Serializer):
    """Сериализация данных от Google"""

    email = serializers.EmailField()
    token = serializers.CharField()


class SocialLinkSerializer(serializers.ModelSerializer):
    """Сериализация данных о социальных ссылках"""

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SocialLink
        fields = ('id', 'link',)


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализация данных об авторе"""

    social_links = SocialLinkSerializer(many=True)

    class Meta:
        model = models.AuthUser
        fields = ('id', 'avatar', 'country', 'city', 'bio', 'display_name', 'social_links')
