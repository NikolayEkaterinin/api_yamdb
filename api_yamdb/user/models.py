from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

MAX_LENGTH_NAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_CODE = 40
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
        max_length=MAX_LENGTH_NAME,
        verbose_name='Логин',
        help_text='Укажите логин',
        unique=True,
        validators=([RegexValidator(regex=r'^[\w.@+-]+$')]))
    email = models.EmailField(max_length=MAX_LENGTH_EMAIL,
                              verbose_name='E-mail',
                              help_text='Укажите e-mail',
                              unique=True)
    confirmation_code = models.CharField(max_length=MAX_LENGTH_CODE,
                                         blank=True,
                                         null=True,
                                         verbose_name='Проверочный код')
    first_name = models.CharField(max_length=MAX_LENGTH_NAME,
                                  verbose_name='Имя',
                                  help_text='Ваше Имя',
                                  blank=True)
    last_name = models.CharField(max_length=MAX_LENGTH_NAME,
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
