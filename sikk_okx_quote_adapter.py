"""OKX OnchainOS 只读报价适配器。

安全原则：本模块只构建 `onchainos swap quote` 命令，不构建 `swap execute`。
"""

from __future__ import annotations

from typing import List

from sikk_execution_adapter_base import QuoteRequest, ReadOnlyQuoteAdapter


class OKXQuoteAdapter(ReadOnlyQuoteAdapter):
    """OKX OnchainOS 只读报价适配器。"""

    source_name = "OKX"

    def build_quote_command(self, request: QuoteRequest) -> List[str]:
        if not request.readable_amount:
            raise ValueError("OKX quote 需要 readable_amount")
        return [
            "onchainos",
            "swap",
            "quote",
            "--from",
            request.input_token,
            "--to",
            request.output_token,
            "--readable-amount",
            str(request.readable_amount),
            "--chain",
            request.chain,
        ]
