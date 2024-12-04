from django.db import models

from apps.common.models import BaseModel
from apps.accounts.models import User


class ShippingAddress(BaseModel):
    """
    Модель адреса доставки пользователя

    Атрибуты:
        user (ForeignKey): Модель пользователя
        full_name (str): Полное имя
        email (str): Email
        phone (str): Телефон
        address (str): адрес
        city (str): Город
        country (str): Страна
        zipcode (int): Почтовый индекс

    Методы:
        __str__: Возвращает информацию об адресе
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shipping_addresses')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        """
        Возвращает информацию об адресе пользователя
        """
        return f'Адрес пользователя {self.full_name}'
