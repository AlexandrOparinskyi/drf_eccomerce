from rest_framework import serializers


class ProfileSerializer(serializers.Serializer):
    """
    Сериализатор профайла пользователя

    Поля:
        first_name(str): Имя пользователя
        last_name(str): Фамилия пользователя
        email(str): Email пользователя. Только для чтения
        avatar(ImageField): Фото пользователя
        account_type(str): Тип аккаунта пользователя. Только для чтения
    """

    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(read_only=True)
    avatar = serializers.ImageField(required=False)
    account_type = serializers.CharField(read_only=True)
