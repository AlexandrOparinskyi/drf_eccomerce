from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.

    Передаются поля:
        email
        password
    Методы:
        validate_password(): Хеширует пароль, перед записью в бд
    """

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_password(self, value: str) -> str:
        return make_password(value)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределение сериализатора получения access_token

    Методы:
        get_token(): Добавляет поля в access_token. Если пользователь
                     является администратором - добавляется поле
                     {group: admin}. Если обычный пользователь -
                     {group: user, role: роль пользователя}
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user.is_staff:
            token['group'] = 'admin'
        else:
            token['group'] = 'user'
            token['role'] = user.account_type

        return token
