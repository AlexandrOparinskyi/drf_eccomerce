from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils import set_dict_attr
from apps.profiles.serializers import ProfileSerializer

tags = ['Profiles']


class ProfileView(APIView):
    """
    Представление пользователя. Доступно 3 метода для получения,
    изменения и удаления

    Методы:
        get(): Получает информацию о пользователе
        put(): Частично изменяет информацию о пользователе.
               Доступно 3 поля - имя, фамилия, фото
        delete(): Меняет статус пользователя is_active на False
    """

    serializer_class = ProfileSerializer

    @extend_schema(
        summary='Получение профиля',
        description='Получение имени, фамилии, email, '
                    'фото и типа пользователя',
        tags=tags
    )
    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Изменение профиля',
        description='Можно изменить имя(first_name), фамилию(last_name)'
                    ' и фото(avatar)',
        tags=tags
    )
    def put(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = set_dict_attr(user, serializer.validated_data)
        user.save()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Удаление профиля',
        description='Статус пользователя is_active становится False',
        tags=tags
    )
    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data={'message': 'Аккаунт удален'})
