"""Cointop models regarding assets and exchange rates"""
from django.contrib.auth import models as auth_models
from django.db import models

from cointop import coinapi


class Alert(models.Model):
    """Alert model"""

    user = models.ManyToManyField(auth_models.User, related_name="alerts")
    asset = models.CharField(
        max_length=7,
        choices=coinapi.get_currencies_for_model(),
        null=False,
    )
    high_low = models.BooleanField(
        choices=((True, "Lower than"), (False, "Higher than")), null=False
    )
    value = models.FloatField(null=False)
