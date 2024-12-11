from django.urls import path

from apps.sellers.views import SellerView

urlpatterns = [
    path('', SellerView.as_view())
]