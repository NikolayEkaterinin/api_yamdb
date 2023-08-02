from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .validators import validate_year
from user.models import User


LETTERS_LIMIT = 15


class Category(models.Model):
    name = models.CharField(
        'Имя категории',
        max_length=200
    )
    slug = models.SlugField(
        'URL категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=200
    )
    slug = models.SlugField(
        'URL жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=200,
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
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]


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
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:LETTERS_LIMIT]
