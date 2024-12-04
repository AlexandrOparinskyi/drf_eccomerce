from django.db import models
from django.utils import timezone


class GetOrNoneQuerySet(models.QuerySet):
    """
    Кастомный Queryset для более удобного применения без блоков try/exept
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExit:
            return None


class GetOrNoneManager(models.Manager):
    """
    Кастомный менеджер с методом get_or_none от GetOrNoneQuerySet
    """
    def get_queryset(self):
        return GetOrNoneQuerySet(self)

    def get_or_none(self, **kwargs):
        return self.get_queryset().get_or_none(**kwargs)


class IsDeletedQuerySet(GetOrNoneQuerySet):
    """
    Кастомный Queryset с измененным удалением
    Если не передан ключ hard_delete, is_deleted записи присваивается True.
    Иначе запись удаляется из базы данных
    """
    def delete(self, hard_delete=False):
        if hard_delete:
            super().delete()
        else:
            return self.update(is_deleted=True, deleted_at=timezone.now())


class IsDeletedManager(GetOrNoneManager):
    """
    Кастомный менеджер. Достает только неудаленные записи.
    Имеет метод, что бы достать все записи
    """
    def get_queryset(self):
        return IsDeletedManager(self.model).filter(is_deleted=False)

    def unfiltered(self):
        return IsDeletedManager(self.model)

    def hard_delete(self):
        return self.get_queryset().delete(hard_delete=True)
