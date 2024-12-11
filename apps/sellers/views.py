from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from unicodedata import category

from apps.common.utils import set_dict_attr
from apps.sellers.models import Seller
from apps.sellers.serializers import SellerSerializer
from apps.shop.models import Products, Category
from apps.shop.serializers import ProductSerializer, CreateProductSerializer

tags = ['Sellers']


class SellerView(APIView):
    serializer_class = SellerSerializer

    @extend_schema(
        summary='Получение статуса продавца',
        description='Для получения статуса продавца',
        tags=tags
    )
    def post(self, request):
        """
        Создание продавца.
        Если пользователь существует, то меняется поле account_type=SELLER
        Если пользователь не существует, создается новый и присваивается
        account_type=SELLER
        """
        user = request.user
        serializer = self.serializer_class(data=request.data, partial=False)
        if serializer.is_valid():
            data = serializer.validated_data
            seller, _ = Seller.objects.update_or_create(user=user,
                                                        defaults=data)
            user.account_type = 'SELLER'
            user.save()
            serializer = self.serializer_class(seller)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductsBySellerView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        summary="Получение товаров",
        description="Получение всех товаров продавца",
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        """
        Получение всех продуктов авторизованного продавца
        """
        user = request.user
        seller = Seller.objects.get_or_none(user=user, is_approved=True)
        products = Products.objects.select_related(
            "category",
            "seller",
            "seller__user"
        ).filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Создание товара",
        description="Создание нового товара",
        tags=tags,
        request=CreateProductSerializer,
        responses=CreateProductSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Создание нового продукта авторизованного продавца.
        """
        serializer = CreateProductSerializer(data=request.data)

        if request.user.seller.is_approved == False:
            return Response(
                data={"message": "Пользователь не является продавцом"},
                status=404
            )

        if serializer.is_valid(raise_exception=False):
            data = serializer.validated_data
            category_slug = data.pop("category_slug", None)
            category = Category.objects.get_or_none(slug=category_slug)
            if not category:
                return Response(data={"message": "Категория не найдена"},
                                status=404)
            data['category'] = category
            data['seller'] = request.user.seller
            new_prod = Products.objects.create(**data)
            serializer = self.serializer_class(new_prod)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class SellerProductView(APIView):
    serializer_class = CreateProductSerializer

    def get_object(self, product_slug):
        product = Products.objects.get_or_none(slug=product_slug)
        return product

    @extend_schema(
        summary='Изменение продукта',
        description='Продукт может поменять только владелец',
        tags=tags
    )
    def put(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('slug'))

        if not product:
            return Response({'message': 'Товар не найден'}, status=404)
        if request.user.seller != product.seller:
            return Response({'message': 'Вы не являетесь владельцем товара'},
                            status=403)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

            if data.get('price_current') != product.price_current:
                product.price_old = product.price_current

            product = set_dict_attr(product, data)
            product.save()
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=200)
        return Response(serializer.data, status=400)

    @extend_schema(
        summary='Удаление продукта',
        description='Продукт может удалить только владелец',
        tags=tags
    )
    def delete(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('slug'))

        if not product:
            return Response({'message': 'Товар не найден'}, status=404)
        if request.user.seller != product.seller:
            return Response({'message': 'Вы не являетесь владельцем товара'},
                            status=403)

        product.delete()
        return Response({'message': 'Товар удален'}, status=204)
