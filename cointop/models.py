"""Cointop models regarding assets and exchange rates"""
from django.contrib.auth import models as auth_models
from django.db import models

from cointop import coinapi


class Alert(models.Model):
    """Alert model"""

    user = models.ManyToManyField(auth_models.User, related_name="alerts")
    asset: models.CharField = models.CharField(
        max_length=7,
        choices=sorted(
            list(coinapi.get_currencies_for_model()), key=lambda item: item[1]
        ),
        null=False,
    )
    high_low: models.BooleanField = models.BooleanField(
        choices=((True, "Lower than"), (False, "Higher than")), null=False
    )
    value: models.FloatField = models.FloatField(null=False)
