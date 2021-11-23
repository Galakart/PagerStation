from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class DirectMessage(models.Model):

    FBITS = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )

    capcode = models.PositiveIntegerField(verbose_name='Капкод', validators=[MaxValueValidator(9999999)])
    freq = models.PositiveIntegerField(verbose_name='Частота (Гц)', validators=[MinValueValidator(60000000), MaxValueValidator(999999999)])
    fbit = models.PositiveSmallIntegerField(choices=FBITS, verbose_name='Бит источника')
    message = models.TextField(max_length=1500, verbose_name='Сообщение')
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.message[:10])
