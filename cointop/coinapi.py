"""CoinAPI wrapper"""
import logging
import time
import typing
import urllib.error

from coinapi_rest_v1 import restapi
from django.core.cache import cache

from admin_cointop import settings
from cointop import coinapi_validation


def get_assets() -> typing.Generator["coinapi_validation.Asset", None, None]:
    """Get crypto list from CoinAPI"""
    _coinapi: "restapi.CoinAPIv1" = restapi.CoinAPIv1(settings.COIN_API_KEY)
    assets = cache.get("coinapi_metadata_list_assets")
    if assets is None:
        try:
            assets = _coinapi.metadata_list_assets()
        except urllib.error.HTTPError:
            logging.error("Too many request to coinapi, waiting 30 seconds")
            time.sleep(30)
            return get_assets()
        cache.set("coinapi_metadata_list_assets", assets, 3600)
    for asset in assets:
        try:
            yield coinapi_validation.Asset(
                asset_id=asset["asset_id"],
                name=asset["name"],
                type_is_crypto=asset["type_is_crypto"],
            )
        except ValueError as _err:
            logging.error("Could now load asset %s: %s", asset["asset_id"], _err)


def get_currencies_for_model() -> typing.Generator[typing.Tuple[str, str], None, None]:
    """Generate currencies currently handled by coinapi"""
    for asset in get_assets():
        if not asset.type_is_crypto:
            yield asset.asset_id, asset.name


def get_exchange_rate(asset: str) -> typing.Optional[float]:
    """Get BTC to currency rate"""
    try:
        _coinapi: "restapi.CoinAPIv1" = restapi.CoinAPIv1(settings.COIN_API_KEY)
    except urllib.error.HTTPError:
        logging.warning("This exchange rate is not available BTC/%s", asset)
        return None
    rate = _coinapi.exchange_rates_get_specific_rate("BTC", asset)
    return rate["rate"]
