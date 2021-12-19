from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

MESSAGE_MAX_LENGTH = 950
CAPCODE_MIN_VALUE = 0
CAPCODE_MAX_VALUE = 9999999
FREQ_MIN_VALUE = 60000000
FREQ_MAX_VALUE = 999999999

FBITS = (
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
)

CODEPAGES = (
    (1, 'lat'),
    (2, 'cyr'),
    (3, 'linguist'),
)

NEWS_CATEGORIES = (
    (1, 'экстренное'),
    (2, 'уведомления'),
    (3, 'новости'),
    (4, 'погода'),
    (5, 'курсы валют'),
    (6, 'юмор'),
    (7, 'гороскоп'),
    (8, 'резерв'),
)


class DirectMessage(models.Model):
    """Отправка сообщения напрямую, с прямым указанием капкода, частоты, источника"""
    capcode = models.PositiveIntegerField(
        verbose_name='Капкод',
        validators=[
            MinValueValidator(CAPCODE_MIN_VALUE),
            MaxValueValidator(CAPCODE_MAX_VALUE),
        ],
    )
    freq = models.PositiveIntegerField(
        verbose_name='Частота (Гц)',
        validators=[
            MinValueValidator(FREQ_MIN_VALUE),
            MaxValueValidator(FREQ_MAX_VALUE),
        ],
    )
    fbit = models.PositiveSmallIntegerField(
        verbose_name='Источник',
        choices=FBITS,
    )
    codepage = models.PositiveSmallIntegerField(
        verbose_name='Кодировка текста',
        choices=CODEPAGES,
    )
    message = models.TextField(
        verbose_name='Сообщение',
        max_length=MESSAGE_MAX_LENGTH,
    )
    date_create = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    is_sent = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.capcode}: {self.message[:10]}'


class Transmitter(models.Model):
    """Передатчики с разными частотами (для разных моделей пейджеров)"""
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
    )
    freq = models.PositiveIntegerField(
        verbose_name='Частота (Гц)',
        validators=[
            MinValueValidator(FREQ_MIN_VALUE),
            MaxValueValidator(FREQ_MAX_VALUE),
        ]
    )

    def __str__(self):
        return self.name


class Pager(models.Model):
    """Параметры конкретного пейджера"""
    subscriber_number = models.PositiveIntegerField(
        verbose_name='Абонентский номер',
        unique=True,
    )
    capcode = models.PositiveIntegerField(
        verbose_name='Приватный капкод',
        validators=[
            MinValueValidator(CAPCODE_MIN_VALUE),
            MaxValueValidator(CAPCODE_MAX_VALUE),
        ]
    )
    fbit = models.PositiveSmallIntegerField(
        verbose_name='Источник',
        choices=FBITS,
    )
    codepage = models.PositiveSmallIntegerField(
        verbose_name='Кодировка текста',
        choices=CODEPAGES,
    )
    transmitter = models.ForeignKey(
        Transmitter,
        on_delete=models.CASCADE,
        verbose_name='Трансмиттер'
    )

    def __str__(self):
        return str(self.subscriber_number)


class Client(models.Model):
    """Клиент и его пейджеры"""
    fio = models.CharField(
        verbose_name='ФИО клиента',
        max_length=200,
    )
    datar = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True,
    )
    pagers = models.ManyToManyField(
        Pager,
        verbose_name='Пейджеры клиента',
    )

    def __str__(self):
        return self.fio


class PrivateMessage(models.Model):
    """Приватное сообщение на пейджер"""
    pager = models.ForeignKey(
        Pager,
        on_delete=models.CASCADE,
        verbose_name='Пейджер-получатель',
    )
    message = models.TextField(
        verbose_name='Сообщение',
        max_length=MESSAGE_MAX_LENGTH,
    )
    date_create = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    is_sent = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.pager.subscriber_number}: {self.message[:10]}'


class NewsChannel(models.Model):
    """Новостные каналы"""
    category = models.PositiveSmallIntegerField(
        verbose_name='Тип рассылки',
        choices=NEWS_CATEGORIES,
    )
    capcode = models.PositiveIntegerField(
        verbose_name='Новостной капкод',
        validators=[
            MinValueValidator(CAPCODE_MIN_VALUE),
            MaxValueValidator(CAPCODE_MAX_VALUE),
        ]
    )
    fbit = models.PositiveSmallIntegerField(
        verbose_name='Источник',
        choices=FBITS,
    )
    codepage = models.PositiveSmallIntegerField(
        verbose_name='Кодировка текста',
        choices=CODEPAGES,
    )
    transmitter = models.ForeignKey(
        Transmitter,
        on_delete=models.CASCADE,
        verbose_name='Трансмиттер'
    )

    def __str__(self):
        return f'{self.transmitter.name}: {self.category}'


class NewsMessage(models.Model):
    """Новостное сообщение"""
    category = models.PositiveSmallIntegerField(
        verbose_name='Тип рассылки',
        choices=NEWS_CATEGORIES,
    )
    message = models.TextField(
        verbose_name='Новостное сообщение',
        max_length=MESSAGE_MAX_LENGTH,
    )
    date_create = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )
    is_sent = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{self.category}: {self.message[:10]}'
