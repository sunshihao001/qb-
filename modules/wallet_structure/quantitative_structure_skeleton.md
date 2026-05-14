# Intel Structure Bot 接口骨架清单

> 说明：本文档只定义代码侧文件名与接口签名，不实现逻辑。目标是让后续实现可以直接按骨架补齐。

## 1. 推荐新增文件

### 量化结构主模块
- `modules/wallet_structure/quantitative_structure_models.py`
- `modules/wallet_structure/dominant_cost_zone_calculator.py`
- `modules/wallet_structure/structure_inventory_estimator.py`
- `modules/wallet_structure/distribution_progress_estimator.py`
- `modules/wallet_structure/markup_motivation_model.py`
- `modules/wallet_structure/counterparty_pressure_quant_model.py`
- `modules/wallet_structure/wallet_pattern_cost_alignment.py`
- `modules/wallet_structure/quantitative_structure_report.py`

### 量化结构输出与契约
- `docs/intel_bot/quantitative_structure_schema_contract.md`
- `docs/intel_bot/intel_structure_bot_index.md`
- `docs/intel_bot/intel_structure_bot_delivery_checklist.md`

## 2. 建议接口签名

### 2.1 `quantitative_structure_models.py`

```python
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional

@dataclass(slots=True)
class DominantCostZoneResult:
    wallet_avg_cost: Optional[float] = None
    same_source_group_cost_low: Optional[float] = None
    same_source_group_cost_mid: Optional[float] = None
    same_source_group_cost_high: Optional[float] = None
    dominant_cost_low: Optional[float] = None
    dominant_cost_mid: Optional[float] = None
    dominant_cost_high: Optional[float] = None
    dominant_cost_confidence: Optional[float] = None
    market_cost_mid: Optional[float] = None
    box_cost_mid: Optional[float] = None
    current_price: Optional[float] = None
    price_to_dominant_cost_pct: Optional[float] = None
    cost_position_status_zh: str = '成本区证据不足'
    cost_evidence_grade_zh: str = '证据不足'
    cost_notes_zh: str = ''

@dataclass(slots=True)
class StructureInventoryEstimateResult:
    structure_max_inventory: Optional[float] = None
    structure_current_inventory: Optional[float] = None
    structure_inventory_remaining_pct: Optional[float] = None
    early_wallet_remaining_pct: Optional[float] = None
    same_source_group_remaining_pct: Optional[float] = None
    top_holder_structure_stability_score: Optional[float] = None
    inventory_status_zh: str = '库存状态未知'
    inventory_notes_zh: str = ''

@dataclass(slots=True)
class DistributionProgressResult:
    structure_sold_pct: Optional[float] = None
    early_wallet_sold_pct: Optional[float] = None
    same_source_group_sold_pct: Optional[float] = None
    distribution_receiver_sold_pct: Optional[float] = None
    backflow_confirmed_pct: Optional[float] = None
    distribution_progress_score: Optional[float] = None
    distribution_progress_status_zh: str = '派发进度未知'
    distribution_notes_zh: str = ''

@dataclass(slots=True)
class MarkupMotivationResult:
    remaining_inventory_score: Optional[float] = None
    unfinished_distribution_score: Optional[float] = None
    cost_position_score: Optional[float] = None
    pattern_control_score: Optional[float] = None
    liquidity_need_score: Optional[float] = None
    second_stage_condition_score: Optional[float] = None
    counterparty_pressure_penalty: Optional[float] = None
    same_source_exit_penalty: Optional[float] = None
    markup_motivation_score: Optional[float] = None
    markup_motivation_status_zh: str = '动机证据不足'
    markup_motivation_notes_zh: str = ''

@dataclass(slots=True)
class CounterpartyPressureResult:
    late_large_buyer_score: Optional[float] = None
    whale_bagholder_score: Optional[float] = None
    retailization_score: Optional[float] = None
    early_to_late_transfer_score: Optional[float] = None
    floating_loss_late_holder_score: Optional[float] = None
    counterparty_pressure_score: Optional[float] = None
    counterparty_pressure_status_zh: str = '对手盘状态未知'
    counterparty_pressure_notes_zh: str = ''

@dataclass(slots=True)
class WalletPatternCostAlignmentResult:
    pattern_type_zh: str = '匹配度未知'
    cost_pattern_match_score: Optional[float] = None
    wallet_behavior_match_score: Optional[float] = None
    alignment_status_zh: str = '匹配度未知'
    alignment_notes_zh: str = ''

@dataclass(slots=True)
class QuantitativeStructureReport:
    token_address: str
    token_symbol: str = ''
    chain: str = 'sol'
    analysis_time: Optional[str] = None
    summary_zh: str = ''
    dominant_cost_zone: Optional[DominantCostZoneResult] = None
    structure_inventory_estimate: Optional[StructureInventoryEstimateResult] = None
    distribution_progress: Optional[DistributionProgressResult] = None
    markup_motivation: Optional[MarkupMotivationResult] = None
    counterparty_pressure: Optional[CounterpartyPressureResult] = None
    wallet_pattern_cost_alignment: Optional[WalletPatternCostAlignmentResult] = None
```

### 2.2 `dominant_cost_zone_calculator.py`

```python
def calculate_dominant_cost_zone(
    *,
    normalized_rows: List[Mapping[str, Any]],
    same_source_groups: List[Mapping[str, Any]],
    current_price: Optional[float] = None,
    market_cost_mid: Optional[float] = None,
    box_cost_mid: Optional[float] = None,
) -> DominantCostZoneResult:
    ...
```

### 2.3 `structure_inventory_estimator.py`

```python
def estimate_structure_inventory(
    *,
    normalized_rows: List[Mapping[str, Any]],
    same_source_groups: List[Mapping[str, Any]],
    dominant_cost_zone: DominantCostZoneResult,
) -> StructureInventoryEstimateResult:
    ...
```

### 2.4 `distribution_progress_estimator.py`

```python
def estimate_distribution_progress(
    *,
    normalized_rows: List[Mapping[str, Any]],
    same_source_groups: List[Mapping[str, Any]],
    transfer_paths: List[Mapping[str, Any]],
    backflow_paths: List[Mapping[str, Any]],
) -> DistributionProgressResult:
    ...
```

### 2.5 `markup_motivation_model.py`

```python
def estimate_markup_motivation(
    *,
    dominant_cost_zone: DominantCostZoneResult,
    structure_inventory: StructureInventoryEstimateResult,
    distribution_progress: DistributionProgressResult,
    counterparty_pressure: CounterpartyPressureResult,
    wallet_pattern_alignment: WalletPatternCostAlignmentResult,
) -> MarkupMotivationResult:
    ...
```

### 2.6 `counterparty_pressure_quant_model.py`

```python
def estimate_counterparty_pressure(
    *,
    normalized_rows: List[Mapping[str, Any]],
    same_source_groups: List[Mapping[str, Any]],
    current_price: Optional[float] = None,
) -> CounterpartyPressureResult:
    ...
```

### 2.7 `wallet_pattern_cost_alignment.py`

```python
def evaluate_wallet_pattern_cost_alignment(
    *,
    dominant_cost_zone: DominantCostZoneResult,
    structure_inventory: StructureInventoryEstimateResult,
    distribution_progress: DistributionProgressResult,
    pattern_hint_zh: str = '匹配度未知',
) -> WalletPatternCostAlignmentResult:
    ...
```

### 2.8 `quantitative_structure_report.py`

```python
def build_quantitative_structure_report(
    *,
    token_address: str,
    token_symbol: str,
    chain: str,
    analysis_time: Optional[str],
    dominant_cost_zone: DominantCostZoneResult,
    structure_inventory: StructureInventoryEstimateResult,
    distribution_progress: DistributionProgressResult,
    markup_motivation: MarkupMotivationResult,
    counterparty_pressure: CounterpartyPressureResult,
    wallet_pattern_cost_alignment: WalletPatternCostAlignmentResult,
) -> QuantitativeStructureReport:
    ...

def write_quantitative_structure_bundle(
    *,
    output_dir: str,
    report: QuantitativeStructureReport,
) -> Dict[str, str]:
    ...
```

## 3. 建议导出方式

可在 `modules/wallet_structure/__init__.py` 中后续补充导出：
- `DominantCostZoneResult`
- `StructureInventoryEstimateResult`
- `DistributionProgressResult`
- `MarkupMotivationResult`
- `CounterpartyPressureResult`
- `WalletPatternCostAlignmentResult`
- `QuantitativeStructureReport`
- `calculate_dominant_cost_zone`
- `estimate_structure_inventory`
- `estimate_distribution_progress`
- `estimate_markup_motivation`
- `estimate_counterparty_pressure`
- `evaluate_wallet_pattern_cost_alignment`
- `build_quantitative_structure_report`
- `write_quantitative_structure_bundle`

## 4. 接入原则

- 这些骨架只能读数据，不应写状态机。
- 所有中文状态应由 `*_zh` 字段输出。
- 不应输出买点或交易执行建议。
- 模块之间通过 dataclass 对象传递，不建议先用松散 dict 黑箱串联。

## 5. 最终约束

这是一份骨架签名文档，不是执行实现。后续如果要落代码，可按这个文件逐个补实现，再把新模块加入 `modules/wallet_structure/__init__.py`。
