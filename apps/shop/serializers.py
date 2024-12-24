from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from django.db import models

from apps.common.utils import avg_rating
from apps.profiles.serializers import ShippingAddressSerializer
from apps.sellers.serializers import SellerSerializer
from apps.shop.models import Products


class CategorySerializer(serializers.Serializer):
    """
    Сериализатор категорий
    """
    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField()


class SellerShopSerializer(serializers.Serializer):
    """
    Сериализатор данных о продавце
    """
    name = serializers.CharField(source="business_name")
    slug = serializers.CharField()
    avatar = serializers.CharField(source="user.avatar")


class ProductSerializer(serializers.Serializer):
    """
    Сериализатор для получения товаров
    """
    seller = SellerShopSerializer()
    name = serializers.CharField()
    slug = serializers.SlugField()
    desc = serializers.CharField()
    price_old = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_current = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = CategorySerializer()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.product_reviews.exists():
            return round(avg_rating(obj.product_reviews.all()), 1)
        return None


class CreateProductSerializer(serializers.Serializer):
    """
    Сериализатор для создания товара
    """
    name = serializers.CharField(max_length=100)
    desc = serializers.CharField()
    price_current = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_slug = serializers.CharField()
    in_stock = serializers.IntegerField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)


class OrderItemProductSerializer(serializers.Serializer):
    """
    Сериализатор информации продукта, добавляемого в корзину
    """
    seller = SellerSerializer()
    name = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='price_current'
    )


class OrderItemSerializer(serializers.Serializer):
    """
    Сериализатор добавленого продукта в корзину
    """
    product = OrderItemProductSerializer()
    quantity = serializers.IntegerField()
    total = serializers.FloatField(source='get_total')


class ToggleCartItemSerializer(serializers.Serializer):
    """
    Сериализатор для валидации данных при добавлении, обновлении
    и удалении товаров из корзины
    """
    slug = serializers.SlugField()
    quantity = serializers.IntegerField()


class CheckoutSerializer(serializers.Serializer):
    """
    Сериализатор для валидации данных на этапе с этапа оформления
    до создания самого заказа
    """
    shipping_id = serializers.UUIDField()


class OrderSerializer(serializers.Serializer):
    """
    Сериализатор для представления данных о заказе
    """
    tx_ref = serializers.CharField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')
    delivery_status = serializers.CharField()
    payment_status = serializers.CharField()
    date_delivered = serializers.DateTimeField()
    shipping_details = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='get_cart_subtotal'
    )
    total = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='get_cart_total'
    )

    @extend_schema_field(ShippingAddressSerializer)
    def get_shipping_details(self, obj):
        return ShippingAddressSerializer(obj).data
