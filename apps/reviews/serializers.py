from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from apps.profiles.serializers import ProfileSerializer
from apps.shop.serializers import ProductSerializer


class ReviewSerializer(serializers.Serializer):
    user = ProfileSerializer()
    product = ProductSerializer()
    rating = serializers.IntegerField(validators=[MinValueValidator(1),
                                                  MaxValueValidator(5)])
    text = serializers.CharField(allow_null=True)


class CreateReviewSerializer(serializers.Serializer):
    rating = serializers.IntegerField(validators=[MinValueValidator(1),
                                                  MaxValueValidator(5)])
    text = serializers.CharField(allow_null=True)
