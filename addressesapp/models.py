from django.db import models
from django.utils import timezone


class Address(models.Model):
    address = models.CharField('адрес', max_length=100, unique=True)
    lat = models.DecimalField(
        'широта',
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    lon = models.DecimalField(
        'долгота',
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField('дата обновления', default=timezone.now)

    class Meta:
        verbose_name = 'адрес'
        verbose_name_plural = 'адреса'

    def __str__(self):
        return self.address
