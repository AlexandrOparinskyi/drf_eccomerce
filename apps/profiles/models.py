from django.db import models

from apps.common.models import BaseModel
from apps.accounts.models import User
from apps.common.utils import generate_unique_code
from apps.shop.models import Products


class ShippingAddress(BaseModel):
    """
    Модель адреса доставки пользователя.
    Наследуется от базовой модели, поэтому имеет 2 дополнительных
    атрибута created_at и updated_at

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


class Order(BaseModel):
    """
        Модель заказа товаров с адресом доставки.
        Наследуется от базовой модели, поэтому имеет 2 дополнительных
        атрибута created_at и updated_at

        Атрибуты:
            ---Детали заказа---
            user (ForeignKey): Пользователь, делающий заказ
            tx_ref (str): Уникальный код. Генерируется с помощью
                          generate_unique_code
            delivery_status  (str/choices): Статус доставки
                                            (DELIVERY_STATUS_CHOICES)
            payment_status (str/choices): Статус оплаты
                                          (PAYMENT_STATUS_CHOICES)

            ---Адрес доставки---
            user (ForeignKey): Модель пользователя
            full_name (str): Полное имя
            email (str): Email
            phone (str): Телефон
            address (str): адрес
            city (str): Город
            country (str): Страна
            zipcode (int): Почтовый индекс

        Методы:
            __str__(): Возвращает информацию об адресе
            save(): Переопределение метода для добавления
                    уникального кода (tx_ref)
        """

    DELIVERY_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("PACKING", "PACKING"),
        ("SHIPPING", "SHIPPING"),
        ("ARRIVING", "ARRIVING"),
        ("SUCCESS", "SUCCESS"),
    )

    PAYMENT_STATUS_CHOICES = (
        ("PENDING", "PENDING"),
        ("PROCESSING", "PROCESSING"),
        ("SUCCESSFUL", "SUCCESSFUL"),
        ("CANCELLED", "CANCELLED"),
        ("FAILED", "FAILED"),
    )

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='orders')
    tx_ref = models.CharField(max_length=100, blank=True, unique=True)
    delivery_status = models.CharField(max_length=20,
                                       default='PENDING',
                                       choices=DELIVERY_STATUS_CHOICES)
    payment_status = models.CharField(max_length=20,
                                       default='PENDING',
                                       choices=PAYMENT_STATUS_CHOICES)

    # Адрес пользователя. Все значение имеют null=True
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zipcode = models.IntegerField(null=True)

    def __str__(self):
        """
        Возвращает информацию об адресе
        """
        return f'{self.user.full_name}`s orders'

    def save(self, *args, **kwargs):
        """
        Переопределение метода save(). Если объект создается
        (self._state.adding), то с помощью функции генерации случайного кода
        tx_ref присваивается этот код
        """
        if self._state.adding:
            self.tx_ref = generate_unique_code(Order, 'tx_ref')
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    """
    Модель продукта в заказе.
    Наследуется от базовой модели, поэтому имеет 2 дополнительных
        атрибута created_at и updated_at

    Атрибуты:
        user (ForeignKey): Пользователь
        order (ForeignKey): Заказ
        product (ForeignKey): Продукт
        quantity (int): Количество продуктов в заказе

    Методы:
        @property get_total(): Вычисляет общую сумму продукта
        __str__(): Возвращает информацию о продукте в заказе
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True)
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='orderitems',
                              null=True,
                              blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def get_total(self):
        """
        Вычисляет общую сумму продукта
        """
        return self.product.price_current * self.quantity

    def __str__(self):
        """
        Возвращает информацию о продукте в заказе
        """
        return str(self.product.name)

    class Meta:
        # Сортировка по дате добавления продуктов в заказ
        ordering = ['-created_at']
