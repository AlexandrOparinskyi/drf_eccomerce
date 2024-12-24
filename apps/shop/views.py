from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.paginations import CustomPagination
from apps.profiles.models import OrderItem, ShippingAddress, Order
from apps.sellers.models import Seller
from apps.shop.filters import ProductFilter
from apps.shop.models import Category, Products
from apps.shop.schema_examples import PRODUCT_PARAM_EXAMPLE
from apps.shop.serializers import (CategorySerializer,
                                   ProductSerializer,
                                   OrderItemSerializer,
                                   ToggleCartItemSerializer,
                                   CheckoutSerializer,
                                   OrderSerializer)

tags = ['Shop']


class CategoriesView(APIView):
    serializer_class = CategorySerializer

    @extend_schema(
        summary='Получение всех категорий',
        description='Получение всех категорий',
        tags=tags
    )
    def get(self, request):
        """
        Получение всех категорий
        """
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Создание категории',
        description='Для создания категории укажите название и картинку',
        tags=tags
    )
    def post(self, request):
        """
        Создание новой категории
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_cat = Category.objects.create(**serializer.validated_data)
            serializer = self.serializer_class(new_cat)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProductsByCategoryView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id="category_products",
        summary='Получение товаров по категории',
        description='Введите slug категории',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        """
        Получение товаров по категориям с помощью slug
        """
        category = Category.objects.get_or_none(slug=kwargs.get('slug'))
        if not category:
            return Response({'message': 'Категория не найдена'}, status=404)
        products = Products.objects.select_related(
            'category',
            'seller',
            'seller__user'
        ).filter(category=category)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=200)


class ProductsView(APIView):
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    @extend_schema(
        operation_id="all_products",
        summary='Получение всех товаров',
        description='Получение всех товаров',
        tags=tags,
        parameters=PRODUCT_PARAM_EXAMPLE
    )
    def get(self, request):
        products = Products.objects.select_related(
            'category',
            'seller',
            'seller__user'
        ).all()
        filterset = ProductFilter(request.GET, queryset=products)
        if filterset.is_valid():
            queryset = filterset.qs
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset,
                                                             request)
            serializer = ProductSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        return Response(filterset.errors, status=400)


class ProductsBySellerView(APIView):
    serializer_class = ProductSerializer

    @extend_schema(
        operation_id='seller_products',
        summary='Получение товаров продавца',
        description='Введите slug продавца',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        seller = Seller.objects.get_or_none(slug=kwargs.get('slug'))
        if not seller:
            return Response({'message': 'Продавец не найден'}, status=404)
        products = Products.objects.select_related(
            'category',
            'seller',
            'seller__user'
        ).filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=200)


class ProductView(APIView):
    serializer_class = ProductSerializer

    def get_object(self, product_slug):
        product = Products.objects.get_or_none(slug=product_slug)
        return product

    @extend_schema(
        operation_id="product_detail",
        summary='Получение товара',
        description='Получение товара по полю slug',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('slug'))
        if not product:
            return Response({'message': 'Товар не найден'}, status=404)
        serializer = self.serializer_class(product)
        return Response(serializer.data, status=200)


class CartView(APIView):
    serializer_class = OrderItemSerializer

    @extend_schema(
        summary='Получение продуктов в корзине',
        description='Получение продуктов в корзине',
        tags=tags
    )
    def get(self, request):
        user = request.user
        orderitem = OrderItem.objects.select_related(
            'product',
            'product__seller',
            'product__seller__user'
        ).filter(user=user, order=None)
        serializer = self.serializer_class(orderitem, many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Изменение товара в корзине',
        description='Добавить/удалить/изменить товар в корзине',
        tags=tags
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = ToggleCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        quantity = data.get('quantity')

        product = Products.objects.select_related(
            'seller__user',
            'seller',
        ).get_or_none(slug=data.get('slug'))
        if not product:
            return Response({'message': 'Товар не найдет'}, status=404)
        orderitem, created = OrderItem.objects.update_or_create(
            user=user,
            order_id=None,
            product=product,
            defaults=({'quantity': quantity})
        )
        resp_message_substring = 'Обновлен'
        status = 200
        if created:
            resp_message_substring = 'Добавлен'
            status = 201
        if orderitem.quantity == 0:
            resp_message_substring = 'Удален'
            orderitem.delete()
            data = None
        if resp_message_substring == 'Удален':
            orderitem.product = product
            serializer = self.serializer_class(orderitem)
            data = serializer.data
        return Response(data={'message': f'Товар {resp_message_substring}',
                              'item': data},
                        status=status)


class CheckoutView(APIView):
    serializer_class = CheckoutSerializer

    @extend_schema(
        summary='Проверка',
        description='Создание заказа',
        tags=tags,
        request=CheckoutSerializer
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        orderitems = OrderItem.objects.filter(user=user, order=None)
        if not orderitems.exists():
            return Response({'message': 'Корзина пуста'}, status=404)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        shipping_id = data.get('shipping_id')
        if shipping_id:
            shipping = ShippingAddress.objects.get_or_none(id=shipping_id)
            if not shipping:
                return Response({'message': 'Нету адреса по этому ID'},
                                status=404)

        def append_shipping_details(shipping):
            fields_to_update = [
                "full_name",
                "email",
                "phone",
                "address",
                "city",
                "country",
                "zipcode",
            ]
            data = {}
            for field in fields_to_update:
                value = getattr(shipping, field)
                data[field] = value
            return data

        order = Order.objects.create(user=user,
                                     **append_shipping_details(shipping))
        orderitems.update(order=order)
        serializer = OrderSerializer(order)
        return Response({'message': 'Успешная проверка',
                        'item': serializer.data},
                        status=200)
