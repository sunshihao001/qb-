import json
from pathlib import Path

from adapters.external_raw_adapter import GMGN_FILES, OKX_FILES, normalize_gmgn, normalize_okx


def test_external_file_maps_exist():
    assert "gmgn_token.json" in GMGN_FILES
    assert "okx_dex_token.json" in OKX_FILES


def test_normalize_gmgn_extracts_required_fields():
    summary = normalize_gmgn([{
        "price_usd": 1,
        "liquidity_usd": 2,
        "volume_1h": 3,
        "holder_count": 4,
        "top_holder_ratio": 0.1,
        "token_age_minutes": 5,
    }])
    assert summary["price.price_usd"] == 1
    assert summary["liquidity.liquidity_usd"] == 2
    assert summary["volume.volume_1h"] == 3


def test_normalize_okx_extracts_quote_fields():
    summary = normalize_okx([{"priceUsd": 1, "liquidityUsd": 2}])
    assert summary["quote.quote_price_usd"] == 1
    assert summary["quote.quote_liquidity_usd"] == 2
