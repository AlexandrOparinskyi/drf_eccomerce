from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.shop.models import Category
from apps.shop.serializers import CategorySerializer

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
