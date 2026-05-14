"""SIKK v0.5 只读实时报价与安全扫描采集器。

本模块只允许调用/构建以下只读命令：
- `gmgn-cli order quote`
- `onchainos swap quote`
- `onchainos security token-scan`

安全边界：不构造、不执行 `gmgn-cli swap`、`gmgn-cli multi-swap`、
`gmgn-cli order strategy create`、`onchainos swap execute` 等真实交易命令。
默认可注入 fake runner 做测试；真实 CLI runner 也只运行上面的只读命令。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from sikk_execution_adapter_base import QuoteRequest, QuoteResult, SecurityScanResult, TokenSide
from sikk_gmgn_quote_adapter import GMGNQuoteAdapter
from sikk_okx_quote_adapter import OKXQuoteAdapter

Runner = Callable[[List[str]], str]

_FORBIDDEN_COMMAND_SNIPPETS = [
    "gmgn-cli swap",
    "gmgn-cli multi-swap",
    "order strategy create",
    "onchainos swap execute",
]

_BOOLEAN_RISK_FIELDS = [
    "isHoneypot",
    "isRubbishAirdrop",
    "isAirdropScam",
    "isHasAssetEditAuth",
    "isLowLiquidity",
    "isDumping",
    "isLiquidityRemoval",
    "isPump",
    "isWash",
    "isFakeLiquidity",
    "isWash2",
    "isFundLinkage",
    "isVeryLowLpBurn",
    "isVeryHighLpHolderProp",
    "isHasBlockingHis",
    "isOverIssued",
    "isCounterfeit",
    "isNotOpenSource",
    "isMintable",
    "isHasFrozenAuth",
    "isNotRenounced",
]


def _assert_readonly_command(command: List[str]) -> None:
    """阻断任何可能广播或创建真实交易/策略的命令。"""

    joined = " ".join(command)
    for snippet in _FORBIDDEN_COMMAND_SNIPPETS:
        if snippet in joined:
            raise ValueError(f"禁止构造/执行真实交易命令：{snippet}")

    allowed_prefixes = (
        ["gmgn-cli", "order", "quote"],
        ["onchainos", "swap", "quote"],
        ["onchainos", "security", "token-scan"],
    )
    if not any(command[: len(prefix)] == prefix for prefix in allowed_prefixes):
        raise ValueError(f"v0.5 采集器只允许只读 quote/token-scan 命令：{command}")


def run_readonly_cli(command: List[str], timeout: int = 30) -> str:
    """运行只读 CLI 命令并返回 stdout。

    注意：本函数会先校验命令白名单；不会运行真实 swap / execute。
    """

    _assert_readonly_command(command)
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
    return completed.stdout


def _loads_json(raw_text: str) -> Dict[str, Any]:
    """解析 CLI 输出 JSON；允许外层不是对象时包装为 raw。"""

    text = (raw_text or "").strip()
    if not text:
        return {}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # 有些 CLI 可能输出说明文字 + JSON；第一版保守保留原文，不猜。
        return {"raw_text": raw_text}
    if isinstance(parsed, dict):
        return parsed
    return {"data": parsed}


def _first_payload_object(payload: Dict[str, Any]) -> Dict[str, Any]:
    """从常见 CLI JSON 包装中取第一层业务对象。"""

    data = payload.get("data", payload)
    if isinstance(data, list):
        return data[0] if data and isinstance(data[0], dict) else {}
    if isinstance(data, dict):
        return data
    return payload


def _pick(row: Dict[str, Any], *keys: str) -> Optional[Any]:
    """按多个可能字段名取第一个非空值。"""

    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return value
    return None


def _parse_pct(value: Any) -> Optional[float]:
    """解析百分比字段，支持 `1.25%`、`1.25`、数字。"""

    if value is None or value == "":
        return None
    try:
        if isinstance(value, str):
            return float(value.strip().rstrip("%"))
        return float(value)
    except (TypeError, ValueError):
        return None


class GMGNLiveQuoteCollector:
    """GMGN 只读实时报价采集器。"""

    source_name = "GMGN"

    def __init__(self) -> None:
        self.adapter = GMGNQuoteAdapter()

    def build_command(self, request: QuoteRequest) -> List[str]:
        command = self.adapter.build_quote_command(request)
        _assert_readonly_command(command)
        return command

    def parse_output(self, raw_text: str, request: QuoteRequest) -> QuoteResult:
        payload = _loads_json(raw_text)
        row = _first_payload_object(payload)
        return QuoteResult(
            source=self.source_name,
            input_token=str(_pick(row, "input_token", "inputToken") or request.input_token),
            output_token=str(_pick(row, "output_token", "outputToken") or request.output_token),
            input_amount=str(_pick(row, "input_amount", "inputAmount") or request.amount_smallest_unit or request.readable_amount or ""),
            output_amount=None if _pick(row, "output_amount", "outputAmount") is None else str(_pick(row, "output_amount", "outputAmount")),
            min_output_amount=None if _pick(row, "min_output_amount", "minOutputAmount") is None else str(_pick(row, "min_output_amount", "minOutputAmount")),
            price_impact_pct=_parse_pct(_pick(row, "price_impact", "priceImpact", "priceImpactPct")),
            raw=payload,
        )

    def collect(self, request: QuoteRequest, runner: Runner = run_readonly_cli) -> QuoteResult:
        command = self.build_command(request)
        return self.parse_output(runner(command), request)


class OKXLiveQuoteCollector:
    """OKX OnchainOS 只读实时报价采集器。"""

    source_name = "OKX"

    def __init__(self) -> None:
        self.adapter = OKXQuoteAdapter()

    def build_command(self, request: QuoteRequest) -> List[str]:
        command = self.adapter.build_quote_command(request)
        _assert_readonly_command(command)
        return command

    def parse_output(self, raw_text: str, request: QuoteRequest) -> QuoteResult:
        payload = _loads_json(raw_text)
        row = _first_payload_object(payload)
        return QuoteResult(
            source=self.source_name,
            input_token=request.input_token,
            output_token=request.output_token,
            input_amount=str(_pick(row, "fromTokenAmount", "input_amount", "inputAmount") or request.readable_amount or request.amount_smallest_unit or ""),
            output_amount=None if _pick(row, "toTokenAmount", "output_amount", "outputAmount") is None else str(_pick(row, "toTokenAmount", "output_amount", "outputAmount")),
            min_output_amount=None if _pick(row, "minReceiveAmount", "min_output_amount", "minOutputAmount") is None else str(_pick(row, "minReceiveAmount", "min_output_amount", "minOutputAmount")),
            price_impact_pct=_parse_pct(_pick(row, "priceImpact", "price_impact", "priceImpactPct")),
            raw=payload,
        )

    def collect(self, request: QuoteRequest, runner: Runner = run_readonly_cli) -> QuoteResult:
        command = self.build_command(request)
        return self.parse_output(runner(command), request)


class OKXSecurityScanCollector:
    """OKX token-scan 只读安全扫描采集器。"""

    source_name = "OKX"

    def build_command(self, *, chain_id: str, token_address: str) -> List[str]:
        command = ["onchainos", "security", "token-scan", "--tokens", f"{chain_id}:{token_address}"]
        _assert_readonly_command(command)
        return command

    def parse_output(self, raw_text: str, *, token_address: str, token_side: TokenSide = TokenSide.BUY) -> SecurityScanResult:
        payload = _loads_json(raw_text)
        row = _first_payload_object(payload)
        triggered = [field for field in _BOOLEAN_RISK_FIELDS if row.get(field) is True]
        return SecurityScanResult(
            source=self.source_name,
            token_address=str(_pick(row, "tokenAddress", "token_address") or token_address),
            token_side=token_side,
            risk_level=str(_pick(row, "riskLevel", "risk_level") or "HIGH").upper(),
            triggered_labels=triggered,
            raw=payload,
        )

    def collect(
        self,
        *,
        chain_id: str,
        token_address: str,
        token_side: TokenSide = TokenSide.BUY,
        runner: Runner = run_readonly_cli,
    ) -> SecurityScanResult:
        command = self.build_command(chain_id=chain_id, token_address=token_address)
        return self.parse_output(runner(command), token_address=token_address, token_side=token_side)


def collect_live_pre_trade_inputs(
    *,
    gmgn_request: Optional[QuoteRequest] = None,
    okx_request: Optional[QuoteRequest] = None,
    okx_chain_id: str = "501",
    scan_token_address: Optional[str] = None,
    scan_token_side: TokenSide = TokenSide.BUY,
    runner: Runner = run_readonly_cli,
) -> Tuple[List[QuoteResult], List[SecurityScanResult]]:
    """采集 v0.5 交易前审查输入。

    返回 `(quote_results, security_scan_results)`，可直接传给 v0.4
    `build_and_write_pre_trade_review`。所有命令均经只读白名单校验。
    """

    quotes: List[QuoteResult] = []
    scans: List[SecurityScanResult] = []

    if gmgn_request is not None:
        quotes.append(GMGNLiveQuoteCollector().collect(gmgn_request, runner=runner))
    if okx_request is not None:
        quotes.append(OKXLiveQuoteCollector().collect(okx_request, runner=runner))
    if scan_token_address:
        scans.append(
            OKXSecurityScanCollector().collect(
                chain_id=okx_chain_id,
                token_address=scan_token_address,
                token_side=scan_token_side,
                runner=runner,
            )
        )
    return quotes, scans


def collect_and_write_live_pre_trade_review(
    *,
    output_dir: str | Path,
    readiness_payload: Dict[str, Any],
    chain: str,
    wallet_address: str,
    human_amount: str,
    gmgn_request: Optional[QuoteRequest] = None,
    okx_request: Optional[QuoteRequest] = None,
    okx_chain_id: str = "501",
    scan_token_address: Optional[str] = None,
    scan_token_side: TokenSide = TokenSide.BUY,
    snapshot_time: Optional[str] = None,
    runner: Runner = run_readonly_cli,
) -> Dict[str, str]:
    """采集只读报价/安全扫描，并接入 v0.4 五文件输出。

    该函数是 v0.5 与 v0.4 的桥接层：
    1. 用 GMGN/OKX 只读命令采集 `QuoteResult` / `SecurityScanResult`；
    2. 调用 `build_and_write_pre_trade_review` 写出五文件；
    3. 全流程不执行真实 swap，不广播交易。
    """

    from sikk_quote_security_review import build_and_write_pre_trade_review

    quote_results, security_scan_results = collect_live_pre_trade_inputs(
        gmgn_request=gmgn_request,
        okx_request=okx_request,
        okx_chain_id=okx_chain_id,
        scan_token_address=scan_token_address,
        scan_token_side=scan_token_side,
        runner=runner,
    )
    return build_and_write_pre_trade_review(
        output_dir=output_dir,
        readiness_payload=readiness_payload,
        chain=chain,
        wallet_address=wallet_address,
        human_amount=human_amount,
        quote_results=quote_results,
        security_scan_results=security_scan_results,
        snapshot_time=snapshot_time,
    )
