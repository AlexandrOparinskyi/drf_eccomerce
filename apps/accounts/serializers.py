from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор создания пользователя
    """

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, value: str) -> str:
        """
        Хеширует пароль с помощью make_password
        """
        return make_password(value)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределение сериализатора получения access_token
    """
    @classmethod
    def get_token(cls, user):
        """
        Добавляет пары {key: value} в access_token
        """
        token = super().get_token(user)

        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'
            token['role'] = user.account_type

        return token
