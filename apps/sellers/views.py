from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.sellers.models import Seller
from apps.sellers.serializers import SellerSerializer

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
