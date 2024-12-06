import secrets
import string

from apps.common.models import BaseModel


def generate_unique_code(model: BaseModel, field: str) -> str:
    allowed_chars = string.ascii_uppercase + string.digits
    unique_code = ''.join(secrets.choice(allowed_chars) for _ in range(12))
    code = unique_code
    similar_object_exists = model.objects.filter(**{field: code}).exists()
    if not similar_object_exists:
        return code
    return generate_unique_code(model, field)
