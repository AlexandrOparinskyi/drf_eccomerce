from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

PRODUCT_PARAM_EXAMPLE = [
    OpenApiParameter(
        name='max_price',
        description='Фильтрация продуктов ниже максимальной цены',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='min_price',
        description='Фильтрация продуктов выше минимальной цены',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='in_stock',
        description='Фильтрация продуктов по количеству',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='created_at',
        description='Фильтрация продуктов по дате создания',
        required=False,
        type=OpenApiTypes.DATE
    ),
    OpenApiParameter(
        name='page',
        description='Страница для пагинации',
        required=False,
        type=OpenApiTypes.INT
    ),
    OpenApiParameter(
        name='page_size',
        description='Отображение количества товаров на странице',
        required=False,
        type=OpenApiTypes.INT
    )
]
