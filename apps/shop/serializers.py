from rest_framework import serializers

from apps.sellers.serializers import SellerSerializer


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
