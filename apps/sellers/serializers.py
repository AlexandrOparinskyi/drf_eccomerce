from rest_framework import serializers


class SellerSerializer(serializers.Serializer):
    """
    Сериализатор продавца

    Поля:
            ---Информация о бизнесе---
        business_name (str): Название бизнеса
        slug (str): Url бизнеса. Только для чтения
        inn_identification_number (str): ИНН бизнеса
        website_url (url): Сайт бизнеса
        phone_number (str): Телефон бизнеса
        business_description (str): Описание бизнеса
            ---Адрес бизнеса---
        business_address (str): Адрес бизнеса
        city (str): Город бизнеса
        postal_code (str): Почтовый индекс бизнеса
            ---Информация о банке
        bank_name (str): Имя банка
        bank_bic_number (int):  БИК банка
        bank_account_number (str): Номер банковского счета
        bank_routing_number (str): Номер банковского счета
            ---Информация о статусе---
        is_approved (bool): Статус, прошел ли продавец проверку.
                            Только для чтения
    """

    business_name = serializers.CharField(max_length=100)
    slug = serializers.CharField(read_only=True)
    inn_identification_number = serializers.CharField(max_length=50)
    website_url = serializers.URLField(required=False, allow_null=True)
    phone_number = serializers.CharField(max_length=12)
    business_description = serializers.CharField()

    business_address = serializers.CharField(max_length=500)
    city = serializers.CharField(max_length=100)
    postal_code = serializers.CharField(max_length=20)

    bank_name = serializers.CharField(max_length=255)
    bank_bic_number = serializers.IntegerField()
    bank_account_number = serializers.CharField(max_length=50)
    bank_routing_number = serializers.CharField(max_length=50)

    is_approved = serializers.BooleanField(read_only=True)
