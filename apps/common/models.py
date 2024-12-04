import uuid

from django.db import models
from django.utils import timezone

from apps.common.managers import GetOrNoneManager, IsDeletedManager


class BaseModel(models.Model):
    """
    Абстрактный класс модели, включающий в себя изменение id
    и общие поля и методы всех моделей

    Атрибуты:
        id (UUIDField): Уникальный идентификатор для каждой модели
        created_at (DateTimeField): Время создания экземпляра
        updated_at (DateTimeField): Время обновления экземпляра
    """

    id = models.UUIDField(default=uuid.uuid4,
                          unique=True,
                          primary_key=True,
                          db_index=True,
                          editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class IsDeletedModel(BaseModel):
    """
    Абстрактный класс модели, который возвращает только
    не удаленные товары с 2-мя методами удаления

    Атрибуты:
        is_deleted (BooleanField): Удален ли товар
        deleted_at (DateTimeField): Когда товар был удален
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = IsDeletedManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
