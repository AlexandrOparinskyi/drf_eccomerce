from django.urls import path

from apps.sellers.views import (SellerView,
                                ProductsBySellerView)

urlpatterns = [
    path('', SellerView.as_view()),
    path("products/", ProductsBySellerView.as_view()),
]
