from django.db import models


class Currency(models.Model):
    """Defines currency model"""
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    plural = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)
    symbol_native = models.CharField(max_length=5)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.code = self.code.upper()
        return super().save(force_insert, force_update, using, update_fields)


class IPLocalization(models.Model):
    """Defines localization model"""
    class IPType(models.TextChoices):
        IP_V4 = 'ipv4'
        IP_V6 = 'ipv6'

    url = models.URLField(verbose_name="URL address", blank=True, null=True, default=None)
    ip = models.GenericIPAddressField(verbose_name="IP address")
    type = models.CharField(verbose_name="IP type: ipv4 or ipv6",
                            max_length=4,
                            choices=IPType.choices,
                            default=IPType.IP_V4)
    latitude = models.DecimalField(max_digits=15, decimal_places=13, blank=True, null=True, default=None)
    longitude = models.DecimalField(max_digits=15, decimal_places=13, blank=True, null=True, default=None)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True, default=None)

