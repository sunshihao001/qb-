# Source & Wallet Intelligence Bot Field Mapping Dictionary

## 1. Purpose
This dictionary defines normalized field names, Chinese meanings, source tiers, interface families, units, time semantics, required status, fallback rules, and downstream model usage.

## 2. Source tiers
- L0: on-chain raw events. Can be fact source.
- L1: GMGN / OKX / wallet API response. Can be fact source.
- L2: SIKK normalized standard product. Can be standardized fact.
- L3: old system zip / historical summary. Historical import sample only.
- L4: dashboard / paper / report / case file. Review or audit only; cannot be reverse fact source.

## 3. Global fields

### token_address
- 中文解释: 代币地址
- 所属数据源: GMGN / OKX / 链上 / legacy import
- 来源接口: token discovery / token basic / holder / trader / quote
- 单位: address string
- 时间含义: none
- 是否必填: yes
- 可否 fallback: no
- 给哪个结构模型使用: all models

### wallet_address
- 中文解释: 钱包地址
- 所属数据源: GMGN holder/trader / 链上 transfer/swap
- 来源接口: wallet holders / traders / transfers / swaps
- 单位: address string
- 时间含义: none
- 是否必填: wallet-level records yes
- 可否 fallback: no
- 给哪个结构模型使用: wallet profile, same-source, funding, backflow, role classification

### source_time
- 中文解释: 源事实时间
- 所属数据源: L0/L1/L2/L3 depending on record
- 来源接口: block time / API provider timestamp / quote timestamp / scan timestamp
- 单位: ISO 8601 UTC
- 时间含义: event or provider fact time
- 是否必填: yes when available; if missing mark missing
- 可否 fallback: only with explicit fallback_used and fallback_source
- 给哪个结构模型使用: temporal integrity, entry timing, same-source timing, snapshot delta

### retrieved_at
- 中文解释: Source Bot 获取数据时间
- 所属数据源: system
- 来源接口: local runtime clock
- 单位: ISO 8601 UTC
- 时间含义: fetch time, not fact event time
- 是否必填: yes
- 可否 fallback: no
- 给哪个结构模型使用: audit / source manifest

### normalized_at
- 中文解释: 标准化产物生成时间
- 所属数据源: system
- 来源接口: local runtime clock
- 单位: ISO 8601 UTC
- 时间含义: normalized file generation time, not event time
- 是否必填: yes
- 可否 fallback: no
- 给哪个结构模型使用: audit / freshness

### raw_response_path
- 中文解释: 原始响应路径
- 所属数据源: local raw archive
- 来源接口: raw response write path
- 单位: path
- 时间含义: none
- 是否必填: yes for L0/L1; optional for L3 imports
- 可否 fallback: no
- 给哪个结构模型使用: audit trace

## 4. Candidate fields
- token_open_time: token/pool open time; source GMGN/OKX/on-chain; required yes; fallback only from pool creation if explicitly marked; used by time models.
- first_seen_at: first Source Bot discovery time; source registry; required yes; no dashboard/paper fallback; used by candidate history and temporal integrity.
- liquidity_usd: current or snapshot liquidity; source GMGN/OKX/quote/security; required for quote/security; fallback from market snapshot with mark; used by liquidity gate handoff.
- holder_count: holder count; source GMGN/on-chain; required for wallet overview; fallback no.

## 5. Kline fields
- kline_open_time: candle open time; source GMGN/OKX; required yes; fallback only close_time - interval.
- kline_close_time: candle close time; source GMGN/OKX; required yes; fallback only open_time + interval.
- open/high/low/close: price OHLC; source GMGN/OKX; required yes; fallback no.
- volume_usd: volume; source GMGN/OKX; required recommended; fallback no.

## 6. Quote/security fields
- quote_requested_at: local request start; source system; required yes; fallback no.
- quote_received_at: local response receive; source system; required yes; fallback no.
- quote_time: quote fact time; source quote provider / block time / pool state; required yes if provider gives; fallback quote_received_at only when marked.
- quote_price: quote price; source OKX/GMGN/quote; required yes; fallback market snapshot only marked.
- security_scan_time: security scan time; source security/GMGN/OKX; required yes if scan performed; fallback retrieved_at only marked.
- security_flags: security flags; source security/GMGN; required yes; fallback empty only if source returned empty.

## 7. Wallet structure fields
- wallet_snapshot_time: holder/trader snapshot time; source GMGN/on-chain; required yes; fallback retrieved_at only marked.
- first_buy_time: first buy event time; source DEX swap / GMGN trader detail; required for cost and entry timing; fallback no if only transfer.
- avg_buy_price: derived from buy amount and token amount; required for active buyers; fallback no for transfer-only wallets.
- funding_source_address: buy-before funding source; source on-chain transfer; required for funding model; fallback no.
- backflow_address: post-sell fund receiver; source on-chain transfer; required if sell exists; fallback no.
- transfer_source_type: active_buy / token_transfer / distribution_receive / airdrop / unknown; used by token source model.
- candidate_group_key: non-final source-side grouping key; source derived evidence; required optional; fallback no.

## 8. Forbidden mappings
- dashboard cannot infer discovered_at.
- paper entry_time cannot infer token_open_time.
- report cannot infer quote_time.
- case file cannot infer wallet_snapshot_time.
- old state_machine cannot enter new state machine.
- old quote/security summary is historical reference only.
