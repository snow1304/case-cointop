"""Cronjobs alerting"""
import logging

from django.contrib.auth import models

from cointop import coinapi


def alert() -> None:
    """Alert user by mail when thresholds are reached"""
    users = models.User.objects.all()
    for user in users:
        alerts = user.alerts.all()
        for _alert in alerts:
            logging.info("Getting exchange rate for BTC to %s", _alert.asset)
            rate = coinapi.get_exchange_rate(_alert.asset)
            if rate is None:
                continue
            if _alert.high_low and rate < _alert.value:  # True = lower than
                logging.info(
                    "ALERT[%s]: BTC to %s is lower than %s",
                    _alert.user,
                    _alert.asset,
                    _alert.value,
                )
            elif not _alert.high_low and rate > _alert.value:
                logging.info(
                    "ALERT[%s]: BTC to %s is higher than %s",
                    _alert.user,
                    _alert.asset,
                    _alert.value,
                )
