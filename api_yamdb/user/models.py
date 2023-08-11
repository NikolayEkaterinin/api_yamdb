from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import (
    MAX_USER_LENGTH,
    MAX_EMAIL_LENGTH,
    MAX_CODE_LENGTH
)

from api_yamdb.validators import validate_username


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLE = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        max_length=MAX_USER_LENGTH,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        validators=[validate_username])
    email = models.EmailField(max_length=MAX_EMAIL_LENGTH,
                              verbose_name='E-mail',
                              help_text='Укажите e-mail',
                              unique=True)
    confirmation_code = models.CharField(max_length=MAX_CODE_LENGTH,
                                         blank=True,
                                         null=True,
                                         verbose_name='Проверочный код')
    first_name = models.CharField(max_length=MAX_USER_LENGTH,
                                  verbose_name='Имя',
                                  help_text='Ваше Имя',
                                  blank=True)
    last_name = models.CharField(max_length=MAX_USER_LENGTH,
                                 verbose_name='Фамилия',
                                 help_text='Ваша Фамилия',
                                 blank=True)
    bio = models.TextField(verbose_name='Биография',
                           help_text='Расскажите о себе',
                           blank=True,)

    role = models.CharField(
        max_length=max(len(role[0]) for role in USER_ROLE),
        verbose_name='Роль',
        choices=USER_ROLE,
        default=USER,
        help_text='Пользователь',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    @property
    def is_admin(self):
        return self.is_staff or self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    def __str__(self):
        return self.username
