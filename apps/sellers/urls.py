from django.urls import path

from apps.sellers.views import (SellerView,
                                ProductsBySellerView, SellerProductView)

urlpatterns = [
    path('', SellerView.as_view()),
    path("products/", ProductsBySellerView.as_view()),
    path('products/detail/<str:slug>/', SellerProductView.as_view())
]
