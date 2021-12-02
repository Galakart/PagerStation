from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

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

MESSAGE_MAX_LENGTH = 1500


class DirectMessage(models.Model):
    """Отправка сообщения напрямую, с прямым указанием капкода, частоты, источника"""
    capcode = models.PositiveIntegerField(verbose_name='Капкод', validators=[
                                          MaxValueValidator(9999999)])
    freq = models.PositiveIntegerField(verbose_name='Частота (Гц)', validators=[
                                       MinValueValidator(60000000), MaxValueValidator(999999999)])
    fbit = models.PositiveSmallIntegerField(
        choices=FBITS, verbose_name='Бит источника')
    message = models.TextField(
        max_length=MESSAGE_MAX_LENGTH, verbose_name='Сообщение')
    date_create = models.DateTimeField(default=timezone.now, editable=False)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.message[:10])


class Transmitter(models.Model):
    """Передатчики с разными частотами (для разных моделей пейджеров)"""
    name = models.CharField(max_length=50, verbose_name='Название', default='')
    freq = models.PositiveIntegerField(verbose_name='Частота (Гц)', validators=[
                                       MinValueValidator(60000000), MaxValueValidator(999999999)])

    def __str__(self):
        return self.name


class Pager(models.Model):
    """Параметры конкретного пейджера"""
    subscriber_number = models.PositiveIntegerField(
        verbose_name='Абонентский номер', unique=True)
    capcode = models.PositiveIntegerField(
        verbose_name='Приватный капкод', validators=[MaxValueValidator(9999999)])
    fbit = models.PositiveSmallIntegerField(
        choices=FBITS, verbose_name='Бит источника')
    codepage = models.PositiveSmallIntegerField(
        choices=CODEPAGES, verbose_name='Тип кодировки')
    transmitter = models.ForeignKey(
        Transmitter, on_delete=models.CASCADE, verbose_name='Трансмиттер')

    def __str__(self):
        return str(self.subscriber_number)


class Client(models.Model):
    """Клиент, и его пейджеры"""
    fio = models.CharField(max_length=200, verbose_name='ФИО клиента')
    datar = models.DateField(
        verbose_name='Дата рождения', blank=True, null=True)
    pagers = models.ManyToManyField(Pager, verbose_name='Пейджеры клиента')

    def __str__(self):
        return self.fio


class PrivateMessage(models.Model):
    """Приватное сообщение на конкретный пейджер"""
    pager = models.ForeignKey(
        Pager, on_delete=models.CASCADE, verbose_name='Пейджер-получатель')
    message = models.TextField(
        max_length=MESSAGE_MAX_LENGTH, verbose_name='Сообщение')
    date_create = models.DateTimeField(default=timezone.now, editable=False)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.message[:10])
