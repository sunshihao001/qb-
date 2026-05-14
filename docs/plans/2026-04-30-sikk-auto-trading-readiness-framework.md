# SIKK Auto Trading Readiness Framework Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 在不直接实盘自动下单的前提下，把现有 SIKK 分析体系升级成“可自动交易前置框架”：自动筛选、自动信号分级、自动仓位建议、自动退出计划、自动模拟交易、自动复盘统计。

**Architecture:** 第一版采用“只读分析 + 纸面交易 + 风控门禁”的分层架构。所有真实交易执行默认禁用，执行层只提供接口占位和人工确认模式，直到模拟交易统计稳定后再接 GMGN/OKX 实盘执行。

**Tech Stack:** Python 3、CSV/JSON 本地文件、现有 `/root/sikk-gmgn/sikk_accumulation_window_detector.py`、`/root/sikk-gmgn/sikk_control_chip_window_detector.py`、后续 GMGN CLI / OKX onchainos 作为数据和执行适配器。

---

## 0. 第一版边界

第一版只做：

- 自动分析
- 自动信号分级
- 自动 BLOCK / PAUSE / ALLOW 判断
- 自动仓位建议
- 自动止损止盈计划
- 自动纸面交易
- 自动复盘统计

第一版不做：

- 不自动实盘买入
- 不自动实盘卖出
- 不读取或保存主钱包私钥
- 不默认启用 GMGN/OKX 真实 swap
- 不输出“必买/必卖/稳赢”

---

## 1. 目标模块结构

建议新增以下文件：

```text
/root/sikk-gmgn/sikk_auto_trade_types.py
/root/sikk-gmgn/sikk_auto_risk_gate.py
/root/sikk-gmgn/sikk_auto_signal_engine.py
/root/sikk-gmgn/sikk_auto_position_sizer.py
/root/sikk-gmgn/sikk_auto_exit_planner.py
/root/sikk-gmgn/sikk_paper_trading_engine.py
/root/sikk-gmgn/sikk_trade_journal.py
/root/sikk-gmgn/sikk_auto_readiness_runner.py
/root/sikk-gmgn/tests/test_sikk_auto_risk_gate.py
/root/sikk-gmgn/tests/test_sikk_auto_signal_engine.py
/root/sikk-gmgn/tests/test_sikk_auto_position_sizer.py
/root/sikk-gmgn/tests/test_sikk_paper_trading_engine.py
```

输出目录：

```text
outputs/auto_readiness/
├── token_readiness_result.json
├── token_readiness_result.csv
├── signal_events.csv
├── paper_trades.csv
├── exit_plan.json
├── risk_gate_report.json
└── auto_readiness_review.md
```

---

## 2. 核心枚举设计

### 2.1 代币执行状态

```text
BLOCK_BUY：禁止买入
PAUSE_NEED_CONFIRM：需要人工确认
ALLOW_PAPER_TRADE：允许纸面交易
ALLOW_SMALL_REAL_WITH_CONFIRM：允许极小仓实盘但必须人工确认
```

### 2.2 信号等级

```text
S0：无信号
S1：观察信号
S2：预备信号
S3：策略观察信号
S4：强确认信号
SX：失效信号
```

### 2.3 策略类型

```text
无策略
SIKK-B 控盘箱体突破回踩
SIKK-B 深洗反转
吸筹窗口突破确认
风险监控
```

### 2.4 风险类型

```text
安全风险
流动性风险
滑点风险
价格影响风险
结构派发风险
钱包清仓风险
数据缺失风险
执行失败风险
系统异常风险
```

---

## 3. Task 1：创建通用数据类型文件

**Objective:** 建立所有自动交易前置模块共享的数据结构，避免后续字段混乱。

**Files:**
- Create: `/root/sikk-gmgn/sikk_auto_trade_types.py`
- Test: `/root/sikk-gmgn/tests/test_sikk_auto_trade_types.py`

**Step 1: 写测试**

验证：

- 信号等级枚举存在
- 风险门禁枚举存在
- readiness 结果可序列化为 JSON

**Step 2: 实现数据类型**

建议包含：

```python
from dataclasses import dataclass, asdict
from enum import Enum
from typing import List, Optional, Dict, Any

class SignalLevel(str, Enum):
    S0 = "S0_无信号"
    S1 = "S1_观察信号"
    S2 = "S2_预备信号"
    S3 = "S3_策略观察信号"
    S4 = "S4_强确认信号"
    SX = "SX_失效信号"

class TradePermission(str, Enum):
    BLOCK_BUY = "BLOCK_BUY_禁止买入"
    PAUSE_NEED_CONFIRM = "PAUSE_NEED_CONFIRM_需要人工确认"
    ALLOW_PAPER_TRADE = "ALLOW_PAPER_TRADE_允许纸面交易"
    ALLOW_SMALL_REAL_WITH_CONFIRM = "ALLOW_SMALL_REAL_WITH_CONFIRM_极小仓实盘需确认"

@dataclass
class RiskGateResult:
    permission: TradePermission
    risk_level: str
    block_reasons: List[str]
    pause_reasons: List[str]
    allow_reasons: List[str]
    missing_evidence: List[str]

@dataclass
class SignalResult:
    signal_level: SignalLevel
    strategy_type: str
    signal_time: Optional[str]
    signal_price: Optional[float]
    confidence_score: float
    evidence: List[str]
    invalidation_reasons: List[str]

@dataclass
class PositionPlan:
    suggested_position_sol: float
    max_position_sol: float
    risk_per_trade_sol: float
    stop_price: Optional[float]
    stop_type: str
    position_reason: str

@dataclass
class ExitPlan:
    hard_stop_price: Optional[float]
    time_stop_minutes: int
    take_profit_rules: List[Dict[str, Any]]
    trailing_stop_rule: Dict[str, Any]
    emergency_exit_rules: List[str]
```

**Step 3: 验证**

Run:

```bash
cd /root/sikk-gmgn && python3 -m py_compile sikk_auto_trade_types.py
```

Expected: 无报错。

---

## 4. Task 2：实现风险门禁模块

**Objective:** 在任何买入信号之前，先判断是否 BLOCK / PAUSE / ALLOW。

**Files:**
- Create: `/root/sikk-gmgn/sikk_auto_risk_gate.py`
- Test: `/root/sikk-gmgn/tests/test_sikk_auto_risk_gate.py`

**输入字段：**

```text
安全风险等级
是否 honeypot
是否可卖
流动性
报价是否可用
预估滑点
价格影响
是否跌破控盘底
是否跌破 AVWAP 放量
早期钱包清仓比例
OBV 状态
CMF 状态
数据是否缺失
```

**BLOCK 规则：**

```text
安全风险 = CRITICAL
honeypot = true
无法卖出
无报价
流动性低于阈值
价格影响 > 10%
滑点 > 20%
跌破控盘底
早期钱包集中清仓
安全扫描失败且当前处于全自动模式
```

**PAUSE 规则：**

```text
安全风险 = HIGH
滑点 10%-20%
价格影响 5%-10%
Top Holder 过度集中
bundler/sniper 占比过高
钱包证据缺失
K线数据延迟
```

**验证命令：**

```bash
cd /root/sikk-gmgn && python3 -m py_compile sikk_auto_risk_gate.py
```

---

## 5. Task 3：实现 S0-S4 / SX 信号引擎

**Objective:** 把控盘箱体、吸筹窗口、钱包状态转换为自动交易前置信号等级。

**Files:**
- Create: `/root/sikk-gmgn/sikk_auto_signal_engine.py`
- Test: `/root/sikk-gmgn/tests/test_sikk_auto_signal_engine.py`

**S3 成立条件：**

```text
第一波控盘箱体明确
close 突破控盘上沿
回踩不破 0% / 0.236 / 0.382
close 重新站上 AVWAP
OBV 不弱
CMF 不持续为负
早期钱包未集中清仓
风险门禁不是 BLOCK
```

**S4 成立条件：**

```text
S3 已成立
放量突破最近 LH
形成 HL → HH
突破 VAH 或接近 T_end 突破确认
OBV / CMF 同步增强
钱包筹码状态健康
风险收益比合格
```

**SX 失效条件：**

```text
跌破控盘底
跌破 POC 且放量
跌破 AVWAP 且放量
早期钱包集中清仓
OBV 持续下降
CMF 持续小于 0
无有效报价或安全升级
```

---

## 6. Task 4：实现仓位建议模块

**Objective:** 根据账户风险、止损距离、信号等级和流动性，生成建议仓位。

**Files:**
- Create: `/root/sikk-gmgn/sikk_auto_position_sizer.py`
- Test: `/root/sikk-gmgn/tests/test_sikk_auto_position_sizer.py`

**第一版固定规则：**

```text
默认模拟账户：10 SOL
单笔风险：0.25%
最大单笔仓位：0.2 SOL
S3 仓位系数：0.5
S4 仓位系数：1.0
PAUSE 状态：仓位 = 0
BLOCK 状态：仓位 = 0
```

**仓位公式：**

```text
风险金额 = 账户权益 × 单笔风险比例
理论仓位 = 风险金额 / 入场价到止损价的百分比距离
最终仓位 = min(理论仓位 × 信号系数 × 流动性系数, 最大单笔仓位)
```

---

## 7. Task 5：实现退出计划模块

**Objective:** 每个纸面买入信号必须同时生成止损、止盈、时间止损、紧急退出规则。

**Files:**
- Create: `/root/sikk-gmgn/sikk_auto_exit_planner.py`
- Test: `/root/sikk-gmgn/tests/test_sikk_auto_exit_planner.py`

**SIKK-B 突破回踩默认退出计划：**

```text
激进止损：控盘 Fib 0.236 下方
正常止损：控盘 Fib 0.382 下方
结构止损：控盘底
时间止损：15-30 分钟未形成 HH，降低评分或退出纸面仓位
止盈 1：+50%，卖 25%
止盈 2：+100%，卖 25%
止盈 3：+200%，卖 25%
剩余：移动止盈，峰值回撤 35%-50%
```

---

## 8. Task 6：实现纸面交易引擎

**Objective:** 不动真钱，用真实 K线后续数据模拟买入、止损、止盈和最终收益。

**Files:**
- Create: `/root/sikk-gmgn/sikk_paper_trading_engine.py`
- Test: `/root/sikk-gmgn/tests/test_sikk_paper_trading_engine.py`

**纸面交易记录字段：**

```text
代币地址
信号时间
策略类型
信号等级
模拟入场价
模拟仓位SOL
止损价
止盈规则
最大浮盈
最大浮亏
最终出场价
最终收益率
最终R倍数
出场原因
是否命中止损
是否命中止盈
```

---

## 9. Task 7：实现交易日志模块

**Objective:** 统一保存每次信号、模拟交易、风险门禁和复盘结果。

**Files:**
- Create: `/root/sikk-gmgn/sikk_trade_journal.py`

**输出：**

```text
outputs/auto_readiness/signal_events.csv
outputs/auto_readiness/paper_trades.csv
outputs/auto_readiness/risk_gate_report.json
outputs/auto_readiness/auto_readiness_review.md
```

---

## 10. Task 8：实现总运行器

**Objective:** 串联已有吸筹窗口、控盘箱体、风险门禁、信号、仓位、退出、纸面交易模块。

**Files:**
- Create: `/root/sikk-gmgn/sikk_auto_readiness_runner.py`

**CLI 示例：**

```bash
python3 /root/sikk-gmgn/sikk_auto_readiness_runner.py \
  --token 6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump \
  --kline /root/sikk-gmgn/data/6AVA_accumulation_test/kline_1m.csv \
  --accumulation-json /root/sikk-gmgn/data/6AVA_accumulation_test/outputs/accumulation_window.json \
  --control-json /root/sikk-gmgn/data/6AVA_accumulation_test/control_outputs/control_chip_window.json \
  --output-dir /root/sikk-gmgn/data/6AVA_accumulation_test/auto_readiness_outputs \
  --mode paper
```

---

## 11. Task 9：用 6AVA 回测验证

**Objective:** 使用已有 6AVA 数据，验证新框架能识别出 16:37 UTC 的 SIKK-B 突破回踩机会，并生成纸面交易结果。

**验证目标：**

```text
信号时间：2026-04-27 16:37:00 UTC
信号等级：S3 或 S4
策略类型：SIKK-B 控盘箱体突破回踩
模拟入场价：接近 0.00023386184
止损参考：0.236 或 0.382
纸面结果：应能捕捉后续 16:52 / 17:02 的上涨空间
```

---

## 12. Task 10：质量门禁

**Objective:** 确保第一版不会误触发真实交易。

**必须检查：**

- [ ] 没有任何默认真实 swap 调用
- [ ] 所有真实执行接口必须 `requires_confirmation=True`
- [ ] `mode=paper` 是默认模式
- [ ] `mode=real` 必须明确传入并且还需要人工确认
- [ ] 安全扫描失败时，全自动模式默认 BLOCK
- [ ] 没有保存私钥
- [ ] 没有打印 API Key
- [ ] 输出中明确写“纸面交易/模拟交易”

---

## 13. 第一版完成标准

第一版完成后，系统应该能回答：

```text
这个代币能不能进入自动交易候选？
当前是 S0/S1/S2/S3/S4/SX 哪个信号？
为什么 BLOCK / PAUSE / ALLOW？
如果只做纸面交易，模拟入场在哪里？
止损在哪里？
止盈怎么分批？
最大可能亏损是多少？
后续真实 K线模拟结果如何？
是否值得进入下一阶段小额实盘测试？
```

---

## 14. 建议执行顺序

```text
1. sikk_auto_trade_types.py
2. sikk_auto_risk_gate.py
3. sikk_auto_signal_engine.py
4. sikk_auto_position_sizer.py
5. sikk_auto_exit_planner.py
6. sikk_paper_trading_engine.py
7. sikk_trade_journal.py
8. sikk_auto_readiness_runner.py
9. 6AVA 回测验证
10. 总结并决定是否进入半自动确认交易阶段
```

---

## 15. 后续版本路线

### v0.1

只做自动交易准备框架 + 纸面交易。

### v0.2

加入 GMGN/OKX 双源报价和安全扫描，但仍不自动实盘。

### v0.3

加入人工确认实盘：系统生成交易计划，你确认后才执行。

### v0.4

极小仓自动实盘：单笔 0.005-0.01 SOL，严格熔断。

### v1.0

多策略、多代币、多钱包、完整风控和历史学习。
