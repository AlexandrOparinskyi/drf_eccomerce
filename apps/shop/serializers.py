from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    """
    Сериализатор категорий

    Поля:
        name (str): Название категории
        slug (str): Url категории. Только для чтения
        image (ImageField): Картинка категории
    """

    name = serializers.CharField(max_length=100)
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField()
