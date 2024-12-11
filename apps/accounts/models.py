from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from apps.accounts.managers import CustomUserManager
from apps.common.models import IsDeletedModel

ACCOUNT_TYPE_CHOICES = (
    ('SELLER', 'SELLER'),
    ('BUYER', 'BUYER')
)


class User(AbstractBaseUser, IsDeletedModel):
    """
    Кастомная модель пользователя с кастомным менеджером CustomUserManager.
    Наследуется от модели IsDeletedModel, которая наследуется от базовой
    модели, поэтому имеет 4 дополнительных атрибута created_at, updated_at,
    is_delete и deleted_at

    Поля:
        first_name (str): Имя пользователя
        last_name (str): Фамилия пользователя
        email (str): Email пользователя
        avatar (ImageField): Фото пользователя
        is_staff (bool): Проверка на доступ к админ-панели
        is_active (bool): Проверка пользователя на актив
        account_type (choices/str): Тип аккаунта (покупатель/продавец)
    Методы:
        full_name(): Возвращает имя и фамилию пользователя
        __str__: Возвращает информацию о пользователе
    """

    first_name = models.CharField(verbose_name='Имя',
                                  max_length=25,
                                  null=True)
    last_name = models.CharField(verbose_name='Фамилия',
                                 max_length=25, null=True)
    email = models.EmailField(verbose_name='Email',
                              unique=True)
    avatar = models.ImageField(verbose_name='Фото',
                               upload_to='avatars/',
                               null=True,
                               default='avatars/default.jpg')
    is_staff = models.BooleanField(verbose_name='Доступ к админке',
                                   default=False)
    is_active = models.BooleanField(verbose_name='Активный', default=True)
    account_type = models.CharField(verbose_name='Тип аккаунта',
                                    max_length=6,
                                    choices=ACCOUNT_TYPE_CHOICES,
                                    default='BUYER')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    @property
    def full_name(self):
        """
        Возвращает имя и фамилию пользователя
        """
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        """
        Возвращает информацию о пользователе
        """
        return self.full_name
