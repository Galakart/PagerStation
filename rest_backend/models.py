from django.db import models


class DirectMessage(models.Model):

    FBITS = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
    )

    capcode = models.CharField(max_length=7, verbose_name='Капкод')
    freq = models.CharField(max_length=9, verbose_name='Частота (Гц)')
    fbit = models.PositiveSmallIntegerField(choices=FBITS, verbose_name='Бит источника')
    message = models.TextField(max_length=1500, verbose_name='Сообщение')
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.message[:10])
