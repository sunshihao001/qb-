"""GMGN 只读报价适配器。

安全原则：本模块只构建 `gmgn-cli order quote` 命令，不构建 `swap`、`multi-swap`、
`order strategy create` 等真实交易命令。
"""

from __future__ import annotations

from typing import List

from sikk_execution_adapter_base import QuoteRequest, ReadOnlyQuoteAdapter


class GMGNQuoteAdapter(ReadOnlyQuoteAdapter):
    """GMGN CLI 只读报价适配器。"""

    source_name = "GMGN"

    def build_quote_command(self, request: QuoteRequest) -> List[str]:
        if not request.amount_smallest_unit:
            raise ValueError("GMGN quote 需要 amount_smallest_unit，不能传 human amount")
        command = [
            "gmgn-cli",
            "order",
            "quote",
            "--chain",
            request.chain,
            "--from",
            request.wallet_address,
            "--input-token",
            request.input_token,
            "--output-token",
            request.output_token,
            "--amount",
            str(request.amount_smallest_unit),
        ]
        if request.slippage is not None:
            command.extend(["--slippage", str(request.slippage)])
        return command
