#!/usr/bin/env bash
set -euo pipefail
PHASE="${1:-full}"
ROOT="/root/sikk-gmgn"
OUT="$ROOT/ai_context"
mkdir -p "$OUT"/{full,index,wallet,cluster,case,telegram,web,runtime,audit,diff}
cd "$ROOT"
case "$PHASE" in
  full)
    repomix --compress --output "$ROOT/ai_context/full/sikk_full_architecture.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  index)
    cat > "$OUT/index/files.txt" <<'FILES'
sikk_unified_view_builder.py
sikkctl.py
sikk_dashboard_site_builder.py
sikk_paper_live_runner.py
sikk_paper_auto_reviewer.py
sikk_paper_explanation_builder.py
tests/test_sikk_unified_view_builder.py
tests/test_sikkctl.py
FILES
    cat "$OUT/index/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/index/sikk_index_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  wallet)
    cat > "$OUT/wallet/files.txt" <<'FILES'
sikk_gmgn_token_report.py
sikk_candidate_wallet_structure_pipeline.py
sikk_wallet_structure_gate.py
sikk_wallet_structure_snapshot.py
sikk_same_source_grouping.py
sikk_wallet_intelligence_adapter.py
sikk_structure_intelligence_fusion.py
tests/test_sikk_wallet_structure_gate.py
FILES
    cat "$OUT/wallet/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/wallet/sikk_wallet_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  cluster)
    cat > "$OUT/cluster/files.txt" <<'FILES'
sikk_okx_cluster_holding_analyzer.py
sikk_okx_cluster_delta.py
sikk_chip_control_state_machine.py
sikk_structure_intelligence_fusion.py
tests/test_sikk_okx_cluster_holding_analyzer.py
FILES
    cat "$OUT/cluster/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/cluster/sikk_cluster_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  case)
    cat > "$OUT/case/files.txt" <<'FILES'
sikk_case_field_source_map.py
sikk_case_data_completeness_auditor.py
sikk_case_data_backfill.py
sikk_paper_explanation_builder.py
FILES
    cat "$OUT/case/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/case/sikk_case_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  telegram)
    cat > "$OUT/telegram/files.txt" <<'FILES'
sikk_telegram_bot_handler.py
sikk_telegram_views.py
sikk_telegram_gateway_adapter.py
tests/test_sikk_telegram_views.py
FILES
    cat "$OUT/telegram/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/telegram/sikk_telegram_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  web)
    cat > "$OUT/web/files.txt" <<'FILES'
sikk_dashboard_site_builder.py
site/app.js
site/index.html
site/style.css
tests/test_sikk_dashboard_site_builder.py
FILES
    cat "$OUT/web/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/web/sikk_web_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  runtime)
    cat > "$OUT/runtime/files.txt" <<'FILES'
sikk_live_run.py
sikk_full_auto_orchestrator.py
sikk_paper_live_runner.py
tests/test_sikk_live_run.py
tests/test_sikk_full_auto_orchestrator.py
FILES
    cat "$OUT/runtime/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/runtime/sikk_runtime_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  audit)
    cat > "$OUT/audit/files.txt" <<'FILES'
sikk_system_audit.py
sikk_explainability_engine.py
sikk_research_loop_controller.py
sikk_gap_detector.py
tests/test_sikk_system_audit.py
tests/test_sikk_research_loop_controller.py
FILES
    cat "$OUT/audit/files.txt" | repomix --stdin --compress --output "$ROOT/ai_context/audit/sikk_audit_context.xml" --ignore "data/**,reports/**,her_tasks/**/reports/**,her_tasks/**/logs/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**,.env,*.env,*key*,*secret*,*token*,*webhook*"
    ;;
  *)
    echo "Unknown phase: $PHASE" >&2
    exit 2
    ;;
esac
