from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import F, Q
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Логин'),
        max_length=150,
        unique=True,
        blank=False,
        help_text=_(
            'Имя пользователя не должно превышать 150 символов, '
            'из спецсимволов разрешены только @/./+/-/_ '),
        validators=[username_validator],
        error_messages={
            'unique': _("Имя пользователя уже существует"),
        }
    )
    email = models.EmailField(
        _('Адрес эл. почты'),
        unique=True,
        blank=False,
        max_length=254,
        error_messages={
            'unique': _("Такой Email уже зарегистрирован"),
        }
    )
    password = models.CharField(_('password'), max_length=150)
    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150)
    is_staff = models.BooleanField(_('Статус администратора'), default=False)
    is_active = models.BooleanField(_('Активный пользователь'), default=True)
    is_admin = models.BooleanField(_('Права администратора'), default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Пописки'
        constraints = (
            models.UniqueConstraint(fields=('user', 'author'),
                                    name='unique following'),
            models.CheckConstraint(check=~Q(user=F('author')),
                                   name='self following')
        )
