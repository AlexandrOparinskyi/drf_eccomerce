from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер для пользователей
    """

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Введите верный email')

    def validate_user(self, first_name, last_name, email):
        if not first_name:
            raise ValueError('У пользователя должно быть имя')

        if not last_name:
            raise ValueError('У пользователя должна быть фамилия')

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError('У пользователя должен быть email')

    def create_user(self, first_name, last_name, email,
                    password, **extra_fields):
        self.validate_user(first_name, last_name, email)

        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=email,
                          **extra_fields)

        user.set_password(password)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_admin', False)
        user.save()
        return user

    def validate_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('После is_staff должно быть True')

        if extra_fields.get('is_admin') is not True:
            raise ValueError('После is_admin должно быть True')

        if not password:
            raise ValueError('У суперпользователя должен быть пароль')

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError('У пользователя отсутствует email')

        return extra_fields

    def create_superuser(self, first_name, last_name, email,
                         password, **extra_fields):
        self.validate_superuser(email, password, **extra_fields)
        user = self.create_user(first_name, last_name, email,
                                password, **extra_fields)
        user.save()
        return user
