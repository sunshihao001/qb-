import json
from pathlib import Path

from sikk_dominant_lifecycle_classifier import (
    classify_lifecycle,
    run_dominant_lifecycle_classifier,
)


def test_active_distribution_from_wallet_block_and_high_counterparty_pressure():
    decision = classify_lifecycle(
        {
            "代币地址": "TokenA",
            "代币符号": "DIST",
            "当前状态": "PAPER_READY",
            "信号等级": "S4_强确认信号",
        },
        {
            "wallet_structure_status": "WALLET_BLOCK",
            "wallet_structure_score": 28,
            "wallet_risk_score": 100,
            "counterparty_pressure_score": 100,
            "data_quality_score": 100,
            "distribution_wallet_count": 4,
            "same_source_sync_sell_score": 75,
            "early_wallet_sold_pct_delta": 16,
            "top10_holder_pct_delta": -6,
            "holder_count_delta_pct": 8,
        },
        {"window_status": "valid", "volume_expansion_score": 75},
        {},
    )

    assert decision["dominant_side_lifecycle"] == "ACTIVE_DISTRIBUTION"
    assert decision["dominant_side_intent"] == "ACTIVE_DISTRIBUTION"
    assert decision["counterparty_state"] == "EXIT_LIQUIDITY_FORMING"
    assert decision["allowed_action"] == "BLOCKED"
    assert decision["would_block_by_lifecycle"] is True
    assert decision["evidence_level"] in {"E3", "E4"}
    assert "alternative_hypothesis" in decision
    assert decision["invalid_conditions"]
    assert decision["chip_control_state"] == "CONTROL_LOST_TO_DISTRIBUTION"
    assert decision["chip_control_action"] == "BLOCK_OR_FORCE_PAPER_EXIT"


def test_second_stage_preparation_from_control_box_without_distribution_conflict():
    decision = classify_lifecycle(
        {
            "代币地址": "TokenB",
            "代币符号": "BOX",
            "当前状态": "WATCHING",
            "信号等级": "S2_预备信号",
        },
        {
            "wallet_structure_status": "WALLET_NEUTRAL",
            "wallet_structure_score": 62,
            "wallet_risk_score": 25,
            "counterparty_pressure_score": 35,
            "data_quality_score": 88,
            "same_source_sync_sell_score": 20,
            "early_wallet_remaining_pct": 45,
            "high_result_remaining_pct": 22,
        },
        {
            "market_pattern_type": "CONTROL_BOX_ACCUMULATION",
            "box_duration_min": 75,
            "price_range_pct": 22,
            "box_compression_score": 70,
            "volume_expansion_score": 55,
            "price_near_control_box_high": True,
        },
        {},
    )

    assert decision["dominant_side_lifecycle"] == "SECOND_STAGE_PREPARATION"
    assert decision["dominant_side_intent"] == "BREAKOUT_TEST"
    assert decision["structure_defense_status"] == "DEFENDING_CONTROL_BOX"
    assert decision["allowed_action"] == "HIGH_PRIORITY_WATCHING"
    assert decision["would_pause_by_lifecycle"] is True
    assert decision["would_block_by_lifecycle"] is False
    assert decision["chip_control_state"] in {"CONTROL_RETAINED_BY_STRUCTURE_SIDE", "CONTROL_UNCLEAR"}
    assert decision["chip_control_action"] != "BLOCK_OR_FORCE_PAPER_EXIT"


def test_reactivation_from_dead_sideways_with_second_stage_valid():
    decision = classify_lifecycle(
        {"代币地址": "TokenC", "代币符号": "OLD", "当前状态": "WATCHING"},
        {
            "wallet_structure_status": "WALLET_NEUTRAL",
            "wallet_structure_score": 55,
            "wallet_risk_score": 20,
            "counterparty_pressure_score": 25,
            "data_quality_score": 80,
        },
        {
            "token_age_min": 180,
            "box_duration_min": 150,
            "volume_expansion_score": 82,
            "second_stage_valid": True,
            "breakout_confirmed": True,
            "wallet_pattern_alignment": "PATTERN_ALIGNED",
        },
        {},
    )

    assert decision["dominant_side_lifecycle"] == "REACTIVATION"
    assert decision["dominant_side_intent"] == "REACTIVATION"
    assert decision["allowed_action"] == "REACTIVATED_BY_SECOND_STAGE"
    assert decision["would_block_by_lifecycle"] is False
    assert decision["chip_control_action"] in {"ALLOW_PAPER_READY_IF_OTHER_GATES_PASS", "OBSERVE_ONLY"}


def test_run_classifier_writes_summary_files(tmp_path):
    root = tmp_path
    state_dir = root / "state_machine"
    wallet_dir = root / "wallet_structure" / "TokenA"
    kline_dir = root / "kline_pipeline"
    signal_dir = root / "candidate_signal_outputs"
    state_dir.mkdir(parents=True)
    wallet_dir.mkdir(parents=True)
    kline_dir.mkdir(parents=True)
    signal_dir.mkdir(parents=True)

    (state_dir / "candidate_states.json").write_text(
        json.dumps(
            {
                "候选状态": [
                    {
                        "代币地址": "TokenA",
                        "代币符号": "DIST",
                        "当前状态": "PAPER_READY",
                        "信号等级": "S4_强确认信号",
                    }
                ]
            },
            ensure_ascii=False,
        )
    )
    (wallet_dir / "wallet_structure_decision.json").write_text(
        json.dumps(
            {
                "代币地址": "TokenA",
                "代币符号": "DIST",
                "wallet_structure_status": "WALLET_BLOCK",
                "wallet_structure_score": 28,
                "wallet_risk_score": 100,
                "counterparty_pressure_score": 100,
                "data_quality_score": 100,
            },
            ensure_ascii=False,
        )
    )
    (kline_dir / "candidate_kline_pipeline_summary.json").write_text(json.dumps({"处理结果": []}, ensure_ascii=False))
    (signal_dir / "candidate_signal_summary.json").write_text(json.dumps({"处理结果": []}, ensure_ascii=False))

    result = run_dominant_lifecycle_classifier(
        candidate_states_path=state_dir / "candidate_states.json",
        wallet_structure_dir=root / "wallet_structure",
        kline_summary_path=kline_dir / "candidate_kline_pipeline_summary.json",
        signal_summary_path=signal_dir / "candidate_signal_summary.json",
        output_dir=root / "lifecycle",
    )

    assert result["统计"]["处理数量"] == 1
    assert (root / "lifecycle" / "dominant_lifecycle_summary.json").exists()
    assert (root / "lifecycle" / "dominant_lifecycle_summary.csv").exists()
    assert (root / "lifecycle" / "dominant_lifecycle_summary.md").exists()
    assert (root / "lifecycle" / "TokenA" / "dominant_lifecycle_decision.json").exists()

    summary = json.loads((root / "lifecycle" / "dominant_lifecycle_summary.json").read_text())
    row = summary["生命周期列表"][0]
    assert row["主导侧生命周期"] == "ACTIVE_DISTRIBUTION"
    assert row["主导侧行为动机"] == "ACTIVE_DISTRIBUTION"
    assert row["允许动作"] == "BLOCKED"
    assert row["筹码控制权状态"] in {"CONTROL_LOST_TO_DISTRIBUTION", "CONTROL_MIGRATING_TO_COUNTERPARTY"}
    assert "本模块只生成生命周期旁路判断" in summary["说明"]
