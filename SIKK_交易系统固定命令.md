# SIKK-GMGN 交易系统固定命令

> 中文说明：本文件固定 SIKK-GMGN / SIKK-SOL 当前阶段的交易系统操作命令。默认全部是候选发现、报价安全、纸面交易、运行面板与复盘命令；不执行真实 swap，不签名，不广播交易。

## 0. 固定工作目录

所有命令默认先进入项目目录：

```bash
cd /root/sikk-gmgn
```

## 1. 启动连续纸面验证主流程（固定主命令）

用途：持续运行候选发现、K线/信号、钱包结构、OKX quote/security、纸面交易、日报和 live dashboard。

```bash
cd /root/sikk-gmgn

python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

中文参数说明：

- `--output-root data/gmgn_candidates_live_run`：固定输出目录。
- `--limit 50`：每轮最多处理 50 个候选。
- `--quote-sources okx`：报价来源固定使用 OKX 只读报价。
- `--default-quote-amount-sol 0.01`：默认报价金额 0.01 SOL。
- `--mode loop`：连续循环运行。
- `--interval-sec 600`：每 600 秒运行一轮。

## 2. 单轮检查命令

用途：只跑一轮，用于测试、排错或手动刷新。

```bash
cd /root/sikk-gmgn

python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode once
```

## 3. 查看后台进程

用途：确认连续交易系统是否仍在运行。

```bash
pgrep -af 'python3 sikk_live_run.py|sikk_live_run.py' || true
```

## 4. 查看实时中文面板

用途：在终端查看 live board 前 200 行。

```bash
cd /root/sikk-gmgn

python3 - <<'PY'
from pathlib import Path
path = Path('data/gmgn_candidates_live_run/live_board.md')
print(path.read_text(encoding='utf-8')[:12000] if path.exists() else 'live_board.md 尚未生成')
PY
```

## 5. 查看核心输出文件是否生成

用途：确认每轮运行产物是否完整。

```bash
cd /root/sikk-gmgn

python3 - <<'PY'
from pathlib import Path
root = Path('data/gmgn_candidates_live_run')
for name in [
    'live_run_manifest.json',
    'live_state.json',
    'live_board.md',
    'live_dashboard.html',
    'events/live_events.jsonl',
]:
    path = root / name
    print(f'{name}: 存在={path.exists()} 大小={path.stat().st_size if path.exists() else 0}')
PY
```

## 6. 查看当前状态统计

用途：快速看 WATCHING / PAPER_READY / PAPER_OPEN / BLOCKED 数量。

```bash
cd /root/sikk-gmgn

python3 - <<'PY'
import json
from pathlib import Path
path = Path('data/gmgn_candidates_live_run/live_state.json')
if not path.exists():
    raise SystemExit('live_state.json 尚未生成')
data = json.loads(path.read_text(encoding='utf-8'))
tokens = data.get('tokens') or data.get('token_statuses') or data.get('candidates') or []
if isinstance(tokens, dict):
    tokens = list(tokens.values())
状态统计 = {}
纸面统计 = {}
报价统计 = {}
安全统计 = {}
for row in tokens:
    状态 = row.get('current_state') or row.get('当前状态') or row.get('state') or 'UNKNOWN'
    状态统计[状态] = 状态统计.get(状态, 0) + 1
    纸面 = (row.get('paper') or {}).get('paper_status') or row.get('paper_status') or 'UNKNOWN'
    报价 = (row.get('quote') or {}).get('quote_gate') or row.get('quote_gate') or 'UNKNOWN'
    安全 = (row.get('security') or {}).get('security_gate') or row.get('security_gate') or 'UNKNOWN'
    纸面统计[纸面] = 纸面统计.get(纸面, 0) + 1
    报价统计[报价] = 报价统计.get(报价, 0) + 1
    安全统计[安全] = 安全统计.get(安全, 0) + 1
print('Token总数:', len(tokens))
print('状态统计:', 状态统计)
print('纸面统计:', 纸面统计)
print('报价统计:', 报价统计)
print('安全统计:', 安全统计)
PY
```

## 7. 查看代币与纸面持仓明细

用途：查看具体代币细节，包括纸面买入时间、代币地址、市值、流动性、24H成交额、纸面买入金额、入场价、当前价、收益率、钱包结构、报价和安全状态。

固定中文入口：

```bash
cd /root/sikk-gmgn
./查询代币明细.sh
```

注意：这里的“买入”是纸面买入/模拟持仓记录，不是真实成交，不执行真实 swap。

## 8. 停止连续运行

用途：需要暂停后台 loop 时使用。先查看 PID，再 kill 指定 PID。

```bash
pgrep -af 'python3 sikk_live_run.py|sikk_live_run.py'
```

然后：

```bash
kill <PID>
```

如果普通停止失败，再使用：

```bash
kill -9 <PID>
```

## 9. 代码与安全验证命令

用途：修改代码后固定执行，确认测试、编译、安全边界通过。

```bash
cd /root/sikk-gmgn

python3 -m pytest \
  tests/test_sikk_live_run.py \
  tests/test_sikk_paper_live_runner.py \
  tests/test_sikk_runtime_v02.py \
  -q

python3 -m py_compile \
  sikk_live_run.py \
  sikk_paper_live_runner.py \
  sikk_live_orchestrator.py \
  sikk_dashboard_builder.py

grep -R "庄家\|gmgn-cli swap\|gmgn-cli multi-swap\|gmgn-cli order strategy create\|order strategy create\|onchainos swap execute\|swap execute\|private key\|api key\|bot_token\|webhook_url" \
  sikk_live_run.py \
  sikk_paper_live_runner.py \
  sikk_live_orchestrator.py \
  sikk_dashboard_builder.py \
  tests/test_sikk_live_run.py \
  tests/test_sikk_paper_live_runner.py \
  tests/test_sikk_runtime_v02.py \
  | cat
```

## 10. 固定阶段流程

当前交易系统固定分阶段如下：

1. `P0_候选发现`
2. `P1_K线吸筹与信号`
3. `P2_钱包结构门禁`
4. `P3_报价安全确认`
5. `P4_live纸面交易`
6. `P5_复盘校准`
7. `P6_人工确认后小额实盘准备`

## 11. 固定安全边界

- 当前主命令只运行纸面交易和观察系统。
- `PAPER_READY` 不是买入授权。
- `WALLET_SUPPORT` 不是买入授权，只表示钱包结构不阻断。
- 缺 quote、缺 security、quote 过期、风险不明，一律不能视为安全。
- 真实交易必须另走确认单、quote/security、人工确认和单独执行层。
- 默认不执行：`gmgn-cli swap`、`gmgn-cli multi-swap`、`order strategy create`、`onchainos swap execute`。
