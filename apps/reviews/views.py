from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsOwner
from apps.common.utils import set_dict_attr
from apps.reviews.models import Review
from apps.reviews.serializers import (CreateReviewSerializer,
                                      ReviewSerializer)
from apps.shop.models import Products

tags = ['Reviews']


class ReviewsAPIView(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, slug):
        return Products.objects.get(slug=slug)

    @extend_schema(
        summary='Получение отзывов',
        description='Получение отзывов определенного товара',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('product_slug'))
        if not product:
            return Response({'message': 'Product not found'},
                            status=404)
        reviews = Review.objects.filter(product=product)
        serializer = self.serializer_class(reviews, many=True)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Создание комментария',
        description='Не забудьте передать slug продукта',
        tags=tags
    )
    def post(self, request, *args, **kwargs):
        product = self.get_object(kwargs.get('product_slug'))
        if not product:
            return Response({'message': 'Product not found'},
                            status=404)
        serializer = CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = Review.objects.create(user=request.user,
                                           product=product,
                                           **serializer.validated_data)
            serializer = self.serializer_class(review)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SingleReviewAPIView(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwner]

    def get_object(self, pk):
        return Review.objects.get(pk=pk)

    @extend_schema(
        summary='Получение отзыва',
        description='Получение отзыва по id',
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        review = self.get_object(kwargs.get('review_id'))
        if not review:
            return Response({'message': 'Review not found'},
                            status=400)
        serializer = self.serializer_class(review)
        return Response(serializer.data, status=200)

    @extend_schema(
        summary='Обновление комментария',
        description='Обновление комментария по id',
        tags=tags
    )
    def put(self, request, *args, **kwargs):
        review = self.get_object(kwargs.get('review_id'))
        if not review:
            return Response({'message': 'Review not found'},
                            status=400)
        serializer = CreateReviewSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            updated_review = set_dict_attr(review, data)
            updated_review.save()
            serializer = self.serializer_class(updated_review)
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        summary='Удаление комментария',
        description='Удаление комментария по id',
        tags=tags
    )
    def delete(self, request, *args, **kwargs):
        review = self.get_object(kwargs.get('review_id'))
        if not review:
            return Response({'message': 'Review not found'},
                            status=400)
        review.is_deleted = True
        review.save()
        return Response(status=204)
