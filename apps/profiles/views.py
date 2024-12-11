from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import serialize

from apps.common.utils import set_dict_attr
from apps.profiles.models import ShippingAddress
from apps.profiles.serializers import (ProfileSerializer,
                                       ShippingAddressSerializer)

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


class ShippingAddressView(APIView):
    """
    Представление адресов пользователя. Доступно 2 метода для
    получения и создания

    Методы:
        get(): Получает адрес пользователя
        post(): Создает новый адрес пользователя
    """

    serializer_class = ShippingAddressSerializer

    @extend_schema(
        summary='Получение адреса пользователя',
        tags=tags
    )
    def get(self, request):
        user = request.user
        shipping_address = ShippingAddress.objects.filter(user=user)
        serializer = self.serializer_class(shipping_address,
                                           many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Создание нового адреса',
        tags=tags
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_address, _ = ShippingAddress.objects.get_or_create(user=user,
                                                                    **data)
        serializer = self.serializer_class(shipping_address)
        return Response(serializer.data, status=201)


class ShippingAddressViewID(APIView):
    """
    Представление для конкретного адреса пользователя по ID.
    Доступно 3 метода, получение, изменение и удаление

    Методы:
        get(address_id): Получение конкретного адреса
        put(address_id): Изменение конкретного адреса
        delete(address_id): Удаление конкретного адреса
    """

    serializer_class = ShippingAddressSerializer

    def get_object(self, user, shipping_id):
        shipping_address = ShippingAddress.objects.get_or_none(id=shipping_id)
        if not shipping_address:
            return Response({'message': 'Адрес с указанным id не найден'})
        return shipping_address

    @extend_schema(
        summary='Получение адреса по id',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs.get('id'))
        serializer = self.serializer_class(shipping_address)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Изменение адреса по id',
        tags=tags
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs.get('id'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_address = set_dict_attr(shipping_address, data)
        shipping_address.save()
        serializer = self.serializer_class(shipping_address)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Удаление адреса по id',
        tags=tags
    )
    def delete(self, request, *args, **kwargs):
        user = request.user
        shipping_address = self.get_object(user, kwargs.get('id'))
        shipping_address.delete()
        return Response({'message': 'Адрес удален'}, status=204)
