import secrets
import string

from apps.common.models import BaseModel
from apps.reviews.models import Review


def generate_unique_code(model: BaseModel, field: str) -> str:
    """
    Генерация уникального id
    """
    allowed_chars = string.ascii_uppercase + string.digits
    unique_code = ''.join(secrets.choice(allowed_chars) for _ in range(12))
    code = unique_code
    similar_object_exists = model.objects.filter(**{field: code}).exists()
    if not similar_object_exists:
        return code
    return generate_unique_code(model, field)


def set_dict_attr(obj, data):
    """
    Добавление каждого измененного атрибута в объект
    """
    for attr, value in data.items():
        setattr(obj, attr, value)
    return obj


def avg_rating(data: list) -> float:
    return sum([i.rating for i in data]) / len(data)
