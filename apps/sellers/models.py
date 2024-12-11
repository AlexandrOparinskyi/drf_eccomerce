from autoslug import AutoSlugField
from django.db import models

from apps.common.models import BaseModel
from apps.accounts.models import User


class Seller(BaseModel):
    """
    Модель продавца, связанного с пользователем.
    Наследуется от базовой модели, поэтому имеет 2 дополнительных
    атрибута created_at и updated_at

    Поля:
            ---Информация о бизнесе---
        user (OneToOneField): Создает связь с пользователем
        business_name (str): Название бизнеса продавца
        slug (AutoSlug): URL-адрес бизнеса. Генерируется автоматически
        inn_identification_number (str): ИНН продавца
        website_url (url): Сайт продавца
        phone_number (str): Телефон продавца
        business_description (str): Описание бизнеса
            ---Адрес---
        business_address (str): Адрес бизнеса
        city (str): Город бизнеса
        postal_code (str): Почтовый индекс
            ---Информация о банке---
        bank_name (str): Название банка
        bank_bic_number (str): БИК банка
        bank_account_number (str): Номер банковского счета
        bank_routing_number (str): Номер банковского счета
            ---Информация о статусе---
        is_approved (bool): Статус, прошел ли продавец проверку

    Методы:
        __str__(): Возвращает информацию о продавце
    """

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='seller')

    # Информация о бизнесе
    business_name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='business_name',
                         always_update=True,
                         null=True)
    inn_identification_number = models.CharField(max_length=50)
    website_url = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    business_description = models.TextField()

    # Адрес
    business_address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

    # Информация о банке
    bank_name = models.CharField(max_length=255)
    bank_bic_number = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=50)
    bank_routing_number = models.CharField(max_length=50)

    # Информация о статусе
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        """
        Возвращает информацию о продавце
        """
        return f'Продавец {self.business_name}'
