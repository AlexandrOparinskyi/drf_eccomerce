from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import (CreateUserSerializer,
                                       MyTokenObtainPairSerializer)


class RegisterAPIView(APIView):
    serializer_class = CreateUserSerializer

    @extend_schema(
        summary='Регистрация пользователя'
    )
    def post(self, request):
        """
        POST-запрос создает пользователя вместе с refresh и access_token
        """
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
    Переопределение представления TokenObtainPairView.
    Необходим для использования своего сериализатора
    """
    serializer_class = MyTokenObtainPairSerializer
