#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Candidate Kline Pipeline

用途：
  从 GMGN 新币筛选输出 `token_candidates.json` 中读取 S3/S2 候选，
  自动拉取 GMGN K线，转换成 SIKK Accumulation Window Detector 可读取的 CSV，
  并可直接运行吸筹窗口识别。

安全边界：
  本模块只调用 `gmgn-cli market kline` 只读行情命令；
  不构建、不执行 swap / strategy / order / onchainos execute 等真实交易命令。
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from sikk_accumulation_window_detector import detect_window, load_csv, write_outputs

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CANDIDATES_PATH = PROJECT_ROOT / "outputs" / "gmgn_new_token_filter" / "token_candidates.json"
DEFAULT_OUTPUT_ROOT = PROJECT_ROOT / "data" / "gmgn_candidates"

FORBIDDEN_COMMAND_SNIPPETS = [
    "gmgn-cli swap",
    "gmgn-cli multi-swap",
    "gmgn-cli order",
    "order strategy create",
    "onchainos swap execute",
    "swap execute",
]

RESOLUTION_MINUTES = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "1h": 60,
    "4h": 240,
    "1d": 1440,
}


def _num(value: Any, default: Optional[float] = None) -> Optional[float]:
    """安全转换数字，兼容 GMGN 字符串数字。"""
    try:
        if value in (None, "", [], {}):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(value: Any, default: Optional[int] = None) -> Optional[int]:
    n = _num(value, None)
    return int(n) if n is not None else default


def _first(row: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """兼容中文字段、英文字段和 GMGN 原始字段。"""
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return value
    return default


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _assert_readonly_kline_command(cmd: List[str]) -> None:
    joined = " ".join(cmd)
    for snippet in FORBIDDEN_COMMAND_SNIPPETS:
        if snippet in joined:
            raise ValueError(f"禁止构建真实交易相关命令：{snippet}")
    if cmd[:3] != ["gmgn-cli", "market", "kline"]:
        raise ValueError("候选 K线管道只允许 gmgn-cli market kline 只读命令")


def build_gmgn_kline_command(
    *,
    token_address: str,
    resolution: str,
    start_ts: int,
    end_ts: int,
    chain: str = "sol",
) -> List[str]:
    """构建 GMGN K线只读命令。

    GMGN `--from` / `--to` 使用 Unix 秒；返回的 `time` 是毫秒。
    """
    if resolution not in RESOLUTION_MINUTES:
        raise ValueError(f"不支持的K线周期：{resolution}")
    if not token_address:
        raise ValueError("缺少代币地址")
    if end_ts <= start_ts:
        raise ValueError("K线结束时间必须晚于开始时间")
    cmd = [
        "gmgn-cli",
        "market",
        "kline",
        "--chain",
        chain,
        "--address",
        token_address,
        "--resolution",
        resolution,
        "--from",
        str(int(start_ts)),
        "--to",
        str(int(end_ts)),
        "--raw",
    ]
    _assert_readonly_kline_command(cmd)
    return cmd


def default_runner(cmd: List[str]) -> Dict[str, Any]:
    """执行 GMGN kline 只读命令并解析 JSON。"""
    _assert_readonly_kline_command(cmd)
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    output = proc.stdout.strip()
    try:
        payload = json.loads(output)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"GMGN kline 输出不是有效 JSON：{output[:1000]}") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"GMGN kline 命令失败：{output[:1000]}")
    return payload


def _extract_kline_rows(raw_payload: Any) -> List[Dict[str, Any]]:
    """兼容 GMGN kline 返回结构：list / {list:[...]} / {data:{list:[...]}}。"""
    if isinstance(raw_payload, list):
        rows = raw_payload
    elif isinstance(raw_payload, dict):
        data = raw_payload.get("data")
        if isinstance(raw_payload.get("list"), list):
            rows = raw_payload["list"]
        elif isinstance(data, dict) and isinstance(data.get("list"), list):
            rows = data["list"]
        elif isinstance(data, list):
            rows = data
        else:
            rows = []
    else:
        rows = []
    return [r for r in rows if isinstance(r, dict)]


def write_kline_csv(*, raw_payload: Any, csv_path: Path | str, supply: Optional[float] = None) -> int:
    """把 GMGN K线 JSON 转成 detector CSV。

    输出字段：timestamp, open, high, low, close, volume, amount, market_cap
    - timestamp：秒级 Unix 时间；GMGN `time` 毫秒自动转秒。
    - volume：USD 成交额，不是 token 数量。
    - market_cap：若有 supply，则 close * supply；否则保留空值。
    """
    rows = _extract_kline_rows(raw_payload)
    normalized: Dict[int, Dict[str, Any]] = {}
    for row in rows:
        ts = _int(_first(row, "time", "timestamp"), None)
        if ts is None:
            continue
        if ts > 10_000_000_000:
            ts = ts // 1000
        open_p = _num(_first(row, "open"), 0.0) or 0.0
        high_p = _num(_first(row, "high"), 0.0) or 0.0
        low_p = _num(_first(row, "low"), 0.0) or 0.0
        close_p = _num(_first(row, "close"), 0.0) or 0.0
        volume = _num(_first(row, "volume"), 0.0) or 0.0
        amount = _num(_first(row, "amount"), None)
        market_cap = close_p * supply if supply else _num(_first(row, "market_cap", "usd_market_cap"), None)
        if open_p <= 0 or high_p <= 0 or low_p <= 0 or close_p <= 0:
            continue
        normalized[int(ts)] = {
            "timestamp": str(int(ts)),
            "open": f"{open_p:.18g}",
            "high": f"{high_p:.18g}",
            "low": f"{low_p:.18g}",
            "close": f"{close_p:.18g}",
            "volume": f"{volume:.18g}",
            "amount": "" if amount is None else f"{amount:.18g}",
            "market_cap": "" if market_cap is None else f"{market_cap:.18g}",
        }

    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["timestamp", "open", "high", "low", "close", "volume", "amount", "market_cap"]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for ts in sorted(normalized):
            writer.writerow(normalized[ts])
    return len(normalized)


def select_candidates_for_kline(
    candidates_path: Path | str,
    *,
    include_levels: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """从 token_candidates.json 读取需要拉 K线的候选。

    默认只处理 `S3_进入SIKK结构分析`；可配置追加 S2。
    """
    levels = include_levels or ["S3_进入SIKK结构分析"]
    payload = json.loads(Path(candidates_path).read_text(encoding="utf-8"))
    rows = payload.get("候选列表", [])
    selected = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        if row.get("筛选等级") in levels and row.get("是否进入候选池", True):
            selected.append(row)
    return selected


def _candidate_address(row: Dict[str, Any]) -> str:
    return str(_first(row, "代币地址", "address", "token_address", default="")).strip()


def _candidate_symbol(row: Dict[str, Any]) -> str:
    return str(_first(row, "代币符号", "symbol", default="UNKNOWN")).strip() or "UNKNOWN"


def _candidate_open_ts(row: Dict[str, Any], fallback_now: Optional[int] = None) -> int:
    """获取候选的开盘锚点。

    优先 open_timestamp / 开盘时间戳；没有时用创建时间；都没有时用当前时间向前 2 小时。
    """
    ts = _int(_first(row, "开盘时间戳", "open_timestamp", "open_ts", "创建时间戳", "created_timestamp", "creation_timestamp"), None)
    if ts is not None:
        return ts
    now = fallback_now or int(datetime.now(timezone.utc).timestamp())
    return now - 7200


def _candidate_supply(row: Dict[str, Any]) -> Optional[float]:
    return _num(_first(row, "总供应量", "total_supply", "circulating_supply", "supply"), None)


def _resolution_duration_minutes(resolution: str, one_minute_minutes: int, five_minute_minutes: int) -> int:
    if resolution == "1m":
        return one_minute_minutes
    if resolution == "5m":
        return five_minute_minutes
    return max(five_minute_minutes, RESOLUTION_MINUTES[resolution] * 100)


def run_accumulation_detector_for_csv(*, token_address: str, csv_path: Path, output_dir: Path, supply: Optional[float] = None) -> Dict[str, Any]:
    """运行已有 SIKK Accumulation Window Detector。"""
    candles = load_csv(str(csv_path), supply=supply)
    result = detect_window(candles, token=token_address, supply=supply)
    write_outputs(result, candles, str(output_dir))
    return result


def run_candidate_kline_pipeline(
    *,
    candidates_path: Path | str = DEFAULT_CANDIDATES_PATH,
    output_root: Path | str = DEFAULT_OUTPUT_ROOT,
    runner: Callable[[List[str]], Dict[str, Any]] = default_runner,
    include_levels: Optional[List[str]] = None,
    resolutions: Optional[List[str]] = None,
    chain: str = "sol",
    one_minute_minutes: int = 120,
    five_minute_minutes: int = 360,
    run_accumulation: bool = True,
) -> Dict[str, Path]:
    """候选池 → GMGN K线 CSV → 吸筹窗口输出 的主流程。"""
    selected = select_candidates_for_kline(candidates_path, include_levels=include_levels)
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    resolutions = resolutions or ["1m", "5m"]
    scan_time = _utc_now()
    results: List[Dict[str, Any]] = []

    for row in selected:
        address = _candidate_address(row)
        if not address:
            continue
        symbol = _candidate_symbol(row)
        supply = _candidate_supply(row)
        start_ts = _candidate_open_ts(row)
        token_dir = output_root / address
        token_dir.mkdir(parents=True, exist_ok=True)

        token_result: Dict[str, Any] = {
            "代币地址": address,
            "代币符号": symbol,
            "筛选等级": row.get("筛选等级"),
            "开盘时间戳": start_ts,
            "输出目录": str(token_dir),
            "K线文件": {},
            "K线数量": {},
            "吸筹窗口输出": None,
            "状态": "ok",
            "错误": "",
        }

        try:
            for resolution in resolutions:
                duration_min = _resolution_duration_minutes(resolution, one_minute_minutes, five_minute_minutes)
                end_ts = start_ts + duration_min * 60
                cmd = build_gmgn_kline_command(
                    token_address=address,
                    resolution=resolution,
                    start_ts=start_ts,
                    end_ts=end_ts,
                    chain=chain,
                )
                raw = runner(cmd)
                raw_path = token_dir / f"gmgn_kline_{resolution}_raw.json"
                raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")
                csv_path = token_dir / f"kline_{resolution}.csv"
                count = write_kline_csv(raw_payload=raw, csv_path=csv_path, supply=supply)
                token_result["K线文件"][resolution] = str(csv_path)
                token_result["K线数量"][resolution] = count

            if run_accumulation and "1m" in resolutions:
                acc_dir = token_dir / "accumulation_outputs"
                acc_result = run_accumulation_detector_for_csv(
                    token_address=address,
                    csv_path=token_dir / "kline_1m.csv",
                    output_dir=acc_dir,
                    supply=supply,
                )
                token_result["吸筹窗口输出"] = str(acc_dir / "accumulation_window.json")
                token_result["吸筹窗口状态"] = acc_result.get("window_status")
                token_result["T_start"] = acc_result.get("T_start")
                token_result["T_end"] = acc_result.get("T_end")
        except Exception as exc:  # 单币失败不影响其他候选
            token_result["状态"] = "error"
            token_result["错误"] = str(exc)
        results.append(token_result)

    summary = {
        "模块": "SIKK 候选币 K线接入管道",
        "扫描时间": scan_time,
        "候选来源": str(candidates_path),
        "处理等级": include_levels or ["S3_进入SIKK结构分析"],
        "处理统计": {
            "读取候选数": len(selected),
            "处理候选数": len(results),
            "成功数量": sum(1 for r in results if r["状态"] == "ok"),
            "失败数量": sum(1 for r in results if r["状态"] != "ok"),
        },
        "处理结果": results,
        "说明": "本管道只读取 GMGN K线并运行吸筹窗口识别，不执行交易。",
    }
    summary_path = output_root / "candidate_kline_pipeline_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"summary_path": summary_path}


def main() -> None:
    parser = argparse.ArgumentParser(description="SIKK 候选币 K线拉取 + 吸筹窗口接入管道")
    parser.add_argument("--candidates", default=str(DEFAULT_CANDIDATES_PATH), help="token_candidates.json 路径")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="候选币K线输出根目录")
    parser.add_argument("--include-s2", action="store_true", help="同时处理 S2_重点观察")
    parser.add_argument("--no-accumulation", action="store_true", help="只拉K线，不运行吸筹窗口识别")
    args = parser.parse_args()

    levels = ["S3_进入SIKK结构分析"]
    if args.include_s2:
        levels.append("S2_重点观察")
    outputs = run_candidate_kline_pipeline(
        candidates_path=args.candidates,
        output_root=args.output_root,
        include_levels=levels,
        run_accumulation=not args.no_accumulation,
    )
    print(json.dumps({k: str(v) for k, v in outputs.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
