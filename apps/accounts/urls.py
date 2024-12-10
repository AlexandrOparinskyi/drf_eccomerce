from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.accounts.views import RegisterAPIView, MyTokenObtainPairView

"""
    '' - url регистрации
    'token/' - url получения access_token
    'token/refresh/' - url получения refresh_token
    'token/verify/' - url проверки access_token
"""
urlpatterns = [
    path('', RegisterAPIView.as_view(), name='registration'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
