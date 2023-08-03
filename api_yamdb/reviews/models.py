from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from user.models import User

from .validators import validate_year


LETTERS_LIMIT = 15
MAX_LENGTH = 200


class BaseModel(models.Model):
    name = models.CharField('Название',
                            max_length=MAX_LENGTH)
    slug = models.SlugField('URL'
                            ,unique=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


class Category(BaseModel):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModel):
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
        max_length=255,
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


class Review(models.Model):
    """Модель отзывов."""
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение для оценки'
    )
    text = models.TextField('Ваш отзыв')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка должна быть от 1'),
            MaxValueValidator(10, message='Оценка должна быть до 10')
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique review'
            )
        ]
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:LETTERS_LIMIT]


class Comments(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Комментируемый отзыв'
    )
    text = models.TextField('Ваш комментарий')
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:LETTERS_LIMIT]
