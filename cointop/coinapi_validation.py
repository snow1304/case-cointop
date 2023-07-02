"""CoinApi Response Validation"""
import pydantic


class Asset(pydantic.BaseModel):
    asset_id: str
    name: str
    type_is_crypto: bool
