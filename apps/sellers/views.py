from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.models import Seller
from apps.sellers.serializers import SellerSerializer
from apps.shop.models import Products, Category
from apps.shop.serializers import ProductSerializer, CreateProductSerializer

tags = ['Sellers']


class SellerView(APIView):
    serializer_class = SellerSerializer

    @extend_schema(
        summary='Меняет статус пользователя на "продавец"',
        description='Для получения статуса продавца',
        tags=tags
    )
    def post(self, request):
        """
        Создание продавца.
        Если пользователь существует, то меняется поле account_type=SELLER
        Если пользователь не существует, создается новый и присваевается
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
        summary="Получение продуктов",
        description="Получение всех продуктов продавца",
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        """
        Получение всех продуктов авторизованного продавца
        """
        seller = Seller.objects.get_or_none(is_approved=True)
        products = Products.objects.select_related(
            "category",
            "seller",
            "seller__user"
        ).filter(seller=seller)
        serializer = self.serializer_class(products, many=True)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Создание продукта",
        description="Создание нового продукта",
        tags=tags,
        request=CreateProductSerializer,
        responses=CreateProductSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Создание нового продукта авторизованного продавца
        """
        serializer = CreateProductSerializer(data=request.data)
        if request.user.seller.is_approved == False:
            return Response(data={"message": "Seller is not approved!"}, status=404)

        if serializer.is_valid(raise_exception=False):
            data = serializer.validated_data
            category_slug = data.pop("category_slug", None)
            category = Category.objects.get_or_none(slug=category_slug)
            if not category:
                return Response(data={"message": "Category does not exist!"}, status=404)
            data['category'] = category
            data['seller'] = request.user.seller
            new_prod = Products.objects.create(**data)
            serializer = ProductSerializer(new_prod)
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
