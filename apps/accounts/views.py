from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import (CreateUserSerializer,
                                       MyTokenObtainPairSerializer)


class RegisterAPIView(APIView):
    """
    Представление для регистрации пользователя

    Методы:
        post(): После проверки полей сериализатором CreateUserSerializer
                добавляет поля в access_token. Если пользователь является
                администратором - добавляется поле {group: admin}.
                Если обычный пользователь -
                {group: user, role: роль пользователя}. При ошибке
                возвращает сообщение ошибки и статус 400
    """
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            if user.is_staff:
                refresh.payload.update({'group': 'admin'})
            else:
                refresh.payload.update({'group': 'user',
                                        'role': user.account_type})

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Переопределение представления TokenObtainPairView для использования
    нужного (своего) сериализатора
    """
    serializer_class = MyTokenObtainPairSerializer
