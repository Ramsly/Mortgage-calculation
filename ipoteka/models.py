from django.db import models


class Ipoteka(models.Model):
    bank_name = models.CharField(max_length=100, default='')
    term_min = models.IntegerField(default=0)
    term_max = models.IntegerField(default=0)
    rate_min = models.FloatField(default=0)
    rate_max = models.FloatField(default=0)
    payment_min = models.BigIntegerField(default=0)
    payment_max = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.bank_name