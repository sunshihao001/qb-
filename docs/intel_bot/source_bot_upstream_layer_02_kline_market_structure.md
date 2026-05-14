# Source Bot 上游数据源分层：第 2 类 K线与市场结构数据

## 定位

第 2 类数据负责把 GMGN / OKX / 本地 K线处理模块的数据整理成盘型识别可直接使用的标准市场结构证据。

用途：

- 盘型识别
- 成本区辅助
- 钱包 × 盘型匹配
- 二段扩张判断

它不负责：

- 判断主导侧动机
- 判断对手盘压力
- 判断派发是否完成
- 输出确定庄家
- 直接触发交易

## 必须采集字段

### 基础字段

- `token_address`
- `timeframe`

### K线窗口字段

- `kline_window_start`
- `kline_window_end`
- `latest_kline_time`

### OHLCV 字段

- `open`
- `high`
- `low`
- `close`
- `volume`

### 成本与结构辅助字段

- `vwap`
- `avwap_if_available`
- `high_low_range`
- `control_box_high`
- `control_box_low`

### 盘型事件字段

- `breakout_time`
- `pullback_time`
- `volume_expansion_ratio`

## 数据来源

- GMGN K线
- OKX K线
- 本地 K线处理模块

## 必须输出

- `kline_normalized.json`
- `market_pattern_source_snapshot.json`

## `kline_normalized.json` 标准结构

每个对象代表一个 token 在一个 timeframe 上的标准 K线窗口摘要。

```json
{
  "token_address": "",
  "timeframe": "1m",
  "kline_window_start": "",
  "kline_window_end": "",
  "latest_kline_time": "",
  "open": 0,
  "high": 0,
  "low": 0,
  "close": 0,
  "volume": 0,
  "vwap": 0,
  "avwap_if_available": null,
  "high_low_range": 0,
  "control_box_high": 0,
  "control_box_low": 0,
  "breakout_time": "",
  "pullback_time": "",
  "volume_expansion_ratio": 0,
  "source_trace": {
    "gmgn_kline": "",
    "okx_kline": "",
    "local_kline_processor": ""
  },
  "field_quality": {
    "missing_required_fields": [],
    "kline_window_status": "",
    "market_structure_status": ""
  }
}
```

## `market_pattern_source_snapshot.json` 标准结构

用途：给盘型识别、成本区辅助、钱包 × 盘型匹配和二段扩张判断提供只读来源快照。

```json
{
  "token_address": "",
  "token_symbol": "",
  "generated_at": "",
  "source_files": {
    "kline_normalized": "",
    "gmgn_kline_raw": {},
    "kline_csv": {},
    "accumulation_window": ""
  },
  "pattern_inputs": {
    "timeframes": [],
    "latest_kline_time": "",
    "control_box_high": 0,
    "control_box_low": 0,
    "breakout_time": "",
    "pullback_time": "",
    "volume_expansion_ratio": 0
  },
  "scope_limits_zh": [
    "本文件只提供盘型识别和钱包匹配所需的市场结构来源快照",
    "不直接判断主导侧动机、对手盘压力或派发是否完成",
    "不输出确定庄家，不触发交易"
  ]
}
```

## 质量规则

- `latest_kline_time` 必须来自实际 K线最后一根 candle。
- `kline_window_start` 必须来自本窗口第一根有效 candle。
- `kline_window_end` 必须来自本窗口最后一根有效 candle。
- `vwap` 必须按窗口内 `close * volume / volume` 加权计算；volume 缺失或为 0 时填 0 并记录质量问题。
- `avwap_if_available` 有本地模块输出时使用，没有时允许为 `null`。
- `control_box_high / control_box_low` 优先使用本地吸筹窗口模块输出；没有时使用窗口 high / low 作为候选结构范围。
- `breakout_time / pullback_time` 只记录事件时间，不做交易结论。
- `volume_expansion_ratio` 只作为市场结构辅助字段，不作为独立买入信号。

## 给钱包证据包的交接字段

后续钱包 × 盘型匹配必须继承：

- `token_address`
- `timeframe`
- `kline_window_start`
- `kline_window_end`
- `latest_kline_time`
- `control_box_high`
- `control_box_low`
- `breakout_time`
- `pullback_time`
- `volume_expansion_ratio`

## 当前代码映射

当前已有基础：

- `sikk_candidate_kline_pipeline.py`
  - 已拉取 GMGN K线
  - 已输出 `kline_1m.csv` / `kline_5m.csv`
  - 已写 GMGN raw K线
  - 已可运行本地 `sikk_accumulation_window_detector`

本次补强目标：

- 输出 `kline_normalized.json`
- 输出 `market_pattern_source_snapshot.json`
- 将 K线窗口、VWAP、箱体、突破/回踩、放量比集中成只读市场结构证据
