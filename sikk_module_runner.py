#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Live Runtime v0.2 模块调用器。

统一调度 K线/钱包/quote/security/paper 模块；单模块失败不会拖死整轮 runtime。
本模块只调用分析/纸面/只读模块，不构造真实 swap。
"""

from __future__ import annotations

import importlib
import subprocess
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping

DEFAULT_BASE_DIR = Path("data/gmgn_candidates_live_run")
MODULE_ORDER = ["kline_signal", "wallet_structure", "quote", "security", "paper_runner"]

_FORBIDDEN_SNIPPETS = [
    "gmgn-cli swap",
    "gmgn-cli multi-swap",
    "order strategy create",
    "onchainos swap execute",
    "swap execute",
]


def _base_dir(config: Mapping[str, Any]) -> Path:
    return Path(str(config.get("base_dir") or DEFAULT_BASE_DIR))


def _token_address(token: Mapping[str, Any]) -> str:
    return str(token.get("token_address") or token.get("代币地址") or "")


def _token_symbol(token: Mapping[str, Any]) -> str:
    return str(token.get("token_symbol") or token.get("代币符号") or token.get("symbol") or "UNKNOWN")


def output_path_for_module(module_key: str, token_address: str, base_dir: Path) -> Path | None:
    mapping = {
        "kline_signal": base_dir / "signals" / token_address / "signal.json",
        "wallet_structure": base_dir / "wallet_structure" / token_address / "wallet_structure_decision.json",
        "quote": base_dir / "quotes" / token_address / "quote.json",
        "security": base_dir / "security" / token_address / "security.json",
    }
    return mapping.get(module_key)


def output_exists_for_module(module_key: str, token_address: str, base_dir: Path) -> bool:
    path = output_path_for_module(module_key, token_address, base_dir)
    return bool(path and path.exists())


def _assert_safe_command(command: List[str]) -> None:
    joined = " ".join(command)
    for snippet in _FORBIDDEN_SNIPPETS:
        if snippet in joined:
            raise ValueError(f"Runtime 禁止真实交易命令：{snippet}")


def default_script_runner(command: List[str]) -> str:
    _assert_safe_command(command)
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=180)
    return completed.stdout


def run_python_function(module_name: str, function_name: str, token: Mapping[str, Any], **kwargs: Any) -> Any:
    module = importlib.import_module(module_name)
    fn = getattr(module, function_name)
    return fn(token, **kwargs)


def run_one_module(
    *,
    module_key: str,
    module_config: Mapping[str, Any],
    token: Mapping[str, Any],
    base_dir: Path,
    force: bool = False,
    script_runner: Callable[[List[str]], str] = default_script_runner,
) -> Dict[str, Any]:
    token_address = _token_address(token)
    token_symbol = _token_symbol(token)

    if not module_config.get("enabled", False):
        return {"module": module_key, "status": "SKIPPED", "reason": "module disabled"}

    if module_key != "paper_runner" and output_exists_for_module(module_key, token_address, base_dir) and not force:
        return {"module": module_key, "status": "SKIPPED", "reason": "output exists"}

    try:
        mode = str(module_config.get("mode") or "script")
        if mode == "python_function":
            run_python_function(
                str(module_config["module_name"]),
                str(module_config["function_name"]),
                token,
                base_dir=base_dir,
            )
        elif mode == "script":
            script_path = str(module_config["script_path"])
            command = ["python3", script_path, "--token", token_address, "--symbol", token_symbol]
            _assert_safe_command(command)
            script_runner(command)
        elif mode == "disabled":
            return {"module": module_key, "status": "SKIPPED", "reason": "module disabled"}
        else:
            return {"module": module_key, "status": "ERROR", "reason": f"unsupported module mode: {mode}"}
        return {"module": module_key, "status": "OK", "reason": "module completed"}
    except Exception as exc:
        return {"module": module_key, "status": "ERROR", "reason": str(exc)}


def run_external_modules_for_token(
    *,
    token: Mapping[str, Any],
    config: Mapping[str, Any],
    force: bool = False,
    script_runner: Callable[[List[str]], str] = default_script_runner,
) -> Dict[str, Any]:
    base_dir = _base_dir(config)
    modules = config.get("modules", {}) if isinstance(config.get("modules", {}), Mapping) else {}
    results: List[Dict[str, Any]] = []

    for module_key in MODULE_ORDER:
        module_config = modules.get(module_key, {"enabled": False})
        results.append(
            run_one_module(
                module_key=module_key,
                module_config=module_config,
                token=token,
                base_dir=base_dir,
                force=force,
                script_runner=script_runner,
            )
        )

    return {
        "token_address": _token_address(token),
        "token_symbol": _token_symbol(token),
        "module_results": results,
        "scope_note": "Runtime 只调度分析/纸面/只读模块，不执行真实 swap。",
    }
