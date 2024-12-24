from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.accounts.models import User
from apps.common.models import IsDeletedModel
from apps.shop.models import Products


class Review(IsDeletedModel):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='reviews')
    product = models.ForeignKey(Products,
                                on_delete=models.CASCADE,
                                related_name='product_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    text = models.TextField(null=True)

    def __str__(self):
        return f'Review by {self.user}'
