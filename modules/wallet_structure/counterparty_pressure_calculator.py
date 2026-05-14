from __future__ import annotations

from typing import Optional

from .quantitative_structure_models import CounterpartyPressureResult


_DEF_WEIGHTS = {
    'late_large_buyer_score': 0.30,
    'whale_bagholder_score': 0.30,
    'retailization_score': 0.15,
    'early_to_late_transfer_score': 0.15,
    'floating_loss_late_holder_score': 0.10,
}


def _clamp_score(value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    return max(0.0, min(float(value), 1.0))


def _status(score: Optional[float]) -> tuple[str, str]:
    if score is None:
        return '对手盘状态未知', '对手盘画像未知'
    if score < 25:
        return '对手盘压力低', '对手盘压力低'
    if score < 55:
        return '对手盘压力中', '对手盘压力中'
    if score < 80:
        return '对手盘压力高', '疑似鲸鱼接盘'
    return '对手盘压力极高', '疑似结构侧派发给对手盘'


def calculate_counterparty_pressure(
    *,
    late_large_buyer_score: Optional[float] = None,
    whale_bagholder_score: Optional[float] = None,
    retailization_score: Optional[float] = None,
    early_to_late_transfer_score: Optional[float] = None,
    floating_loss_late_holder_score: Optional[float] = None,
) -> CounterpartyPressureResult:
    """Quantify counterparty pressure from late-stage buyer / bagholder evidence."""
    components = {
        'late_large_buyer_score': _clamp_score(late_large_buyer_score),
        'whale_bagholder_score': _clamp_score(whale_bagholder_score),
        'retailization_score': _clamp_score(retailization_score),
        'early_to_late_transfer_score': _clamp_score(early_to_late_transfer_score),
        'floating_loss_late_holder_score': _clamp_score(floating_loss_late_holder_score),
    }
    present = [v for v in components.values() if v is not None]
    if not present:
        return CounterpartyPressureResult(
            **components,
            counterparty_pressure_score=0.0,
            counterparty_pressure_status_zh='对手盘压力低',
            counterparty_pressure_profile_zh='对手盘压力低',
            counterparty_pressure_notes_zh='缺少晚期大额买入、接盘鲸鱼、散户化和浮亏钱包证据，默认压力偏低。',
        )

    score = round(
        sum((components[key] or 0.0) * _DEF_WEIGHTS[key] for key in _DEF_WEIGHTS) * 100.0,
        2,
    )
    score = round(min(100.0, score + 0.4 * len(present)), 2)
    status_zh, profile_zh = _status(score)
    return CounterpartyPressureResult(
        **components,
        counterparty_pressure_score=score,
        counterparty_pressure_status_zh=status_zh,
        counterparty_pressure_profile_zh=profile_zh,
        counterparty_pressure_notes_zh='对手盘压力总分 = 晚期大额买入 + 接盘鲸鱼 + 散户化 + 早晚期转移 + 浮亏晚持分项的加权汇总。',
    )


__all__ = ['calculate_counterparty_pressure']
