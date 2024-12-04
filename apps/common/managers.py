from django.db import models
from django.utils import timezone


class GetOrNoneQuerySet(models.QuerySet):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExit:
            return None


class GetOrNoneManager(models.Manager):
    def get_queryset(self):
        return GetOrNoneQuerySet(self)

    def get_or_none(self, **kwargs):
        return self.get_queryset().get_or_none(**kwargs)


class IsDeletedQuerySet(GetOrNoneQuerySet):
    def delete(self, hard_delete=False):
        if hard_delete:
            super().delete()
        else:
            return self.update(is_deleted=True, deleted_at=timezone.now())


class IsDeletedManager(GetOrNoneManager):
    def get_queryset(self):
        return IsDeletedManager(self.model).filter(is_deleted=False)

    def unfiltered(self):
        return IsDeletedManager(self.model)

    def hard_delete(self):
        return self.get_queryset().delete(hard_delete=True)
