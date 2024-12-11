from attr.validators import max_len
from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    """
    Сериализатор профайла пользователя

    Поля:
        first_name (str): Имя пользователя
        last_name (str): Фамилия пользователя
        email (str): Email пользователя. Только для чтения
        avatar (ImageField): Фото пользователя
        account_type (str): Тип аккаунта пользователя. Только для чтения
    """

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(read_only=True)
    avatar = serializers.ImageField(required=False)
    account_type = serializers.CharField(read_only=True)


class ShippingAddressSerializer(serializers.Serializer):
    """
    Сериализатор адреса доставки пользователя

    Поля:
        id (uuid): Идентификационный номер адреса
        full_name (str): Полные фамилия и имя пользователя
        email (str): Email пользователя
        phone (str): Телефон пользователя
        address (str): Адрес доставки пользователя
        city (str): Город доставки пользователя
        country (str): Страна доставки пользователя
        zipcode (int): Почтовый индекс
    """

    id = serializers.UUIDField(read_only=True)
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=12)
    address = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=100)
    zipcode = serializers.IntegerField()
