from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceWalletBotConfig:
    """Filesystem configuration for Source Wallet Bot.

    Paths are deliberately isolated under modules/source_wallet_bot and
    data/source_wallet_bot to avoid touching state machine, paper runner, or
    execution layers.
    """

    project_root: Path = Path("/root/sikk-gmgn")

    @property
    def module_dir(self) -> Path:
        return self.project_root / "modules" / "source_wallet_bot"

    @property
    def data_dir(self) -> Path:
        return self.project_root / "data" / "source_wallet_bot"

    @property
    def schema_dir(self) -> Path:
        return self.data_dir / "schemas"

    @property
    def audit_dir(self) -> Path:
        return self.data_dir / "audit"

    @property
    def reports_dir(self) -> Path:
        return self.project_root / "reports" / "source_wallet_bot"

    @property
    def checkpoints_dir(self) -> Path:
        return self.project_root / "research_loop" / "checkpoints"


ALLOWED_SOURCE_LEVELS = {"L0", "L1", "L2", "L3", "L4"}
FACT_SOURCE_LEVELS = {"L0", "L1", "L2"}
LEGACY_ONLY_LEVELS = {"L3", "L4"}

FORBIDDEN_HANDOFF_FIELDS = {
    "PAPER_READY",
    "BLOCKED",
    "final_trade_gate",
    "dominant_side_control",
    "second_rally_motive",
    "buyability",
    "real_execution_action",
}

ALLOWED_EVIDENCE_LABELS = {
    "疑似结构执行钱包",
    "疑似同源执行组",
    "疑似分发接收钱包",
    "疑似派发钱包",
    "疑似利润回收钱包",
    "疑似核心资金源候选",
    "疑似接盘鲸鱼",
    "疑似结果钱包",
    "证据不足",
    "字段缺失",
    "需要链上补查",
}
