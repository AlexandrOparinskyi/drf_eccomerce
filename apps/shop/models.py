from autoslug import AutoSlugField
from django.db import models

from apps.common.models import BaseModel, IsDeletedModel
from apps.sellers.models import Seller


class Category(BaseModel):
    """
    Модель категорий товаров.
    Наследуется от базовой модели, поэтому имеет 2 дополнительных
    атрибута created_at и updated_at

    Атрибуты:
        name (str): Название категории
        slug (slug): URL-адрес категории. Генерируется автоматически
        image (ImageField): Картинка категории

    Методы:
        __str__(): Возвращает информацию о категории
    """

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name',
                         unique=True,
                         always_update=True)
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        """
        Возвращает информацию о категории
        """
        return str(self.name)

    class Meta:
        verbose_name_plural = 'Categories'


class Products(IsDeletedModel):
    """
    Модель продуктов.
    Наследуется от модели IsDeletedModel, которая наследуется от базовой
    модели, поэтому имеет 4 дополнительных атрибута created_at, updated_at,
    is_delete и deleted_at

    Атрибуты:
        seller (ForeignKey): Продавец
        name (str): Название продукта
        slug (url): URL-адрес продукты. Генерируется автоматически
        desc (str): Описание продукта
        price_old (Decimal): Старая цена продукта
        price_current (Decimal): Опциональная цена продукта
        category(ForeignKey): Категория продукта
        in_stock (int): Количество продуктов на складе
        image1, image2, image3 (ImageField): Картинки продукта

    Методы:
        __str__(): Возвращает информацию о продукте
    """

    seller = models.ForeignKey(Seller,
                               on_delete=models.SET_NULL,
                               related_name='products',
                               null=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
    desc = models.TextField()
    price_old = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    price_current = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    in_stock = models.IntegerField(default=5)

    # Картинки продукта
    image1 = models.ImageField(upload_to='products_image/')
    image2 = models.ImageField(upload_to='products_image/', blank=True)
    image3 = models.ImageField(upload_to='products_image/', blank=True)

    def __str__(self):
        """
        Возвращает информацию о продукте
        """
        return str(self.name)
