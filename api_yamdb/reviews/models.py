from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from user.models import User
from api_yamdb.settings import LETTERS_LIMIT, MAX_LENGTH

from api_yamdb.validators import validate_year


class NameSlugBaseModel(models.Model):
    name = models.CharField('Название',
                            max_length=MAX_LENGTH)
    slug = models.SlugField('URL',
                            unique=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Category(NameSlugBaseModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(NameSlugBaseModel):
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH,
        db_index=True
    )
    year = models.IntegerField(
        'Год выхода',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name', 'year']),
            models.Index(fields=['name'], name='name_idx'),
        ]

    def __str__(self):
        return self.name


class BaseModelData(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:LETTERS_LIMIT]


class Review(BaseModelData):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение для оценки'
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1, message='Оценка должна быть от 1'),
            MaxValueValidator(10, message='Оценка должна быть до 10')
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class Comments(BaseModelData):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
