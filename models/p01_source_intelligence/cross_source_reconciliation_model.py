"""P01 source intelligence model stub for cross_source_reconciliation_model.

The canonical orchestration lives in controllers/p01_data_source_intelligence_controller.py.
These modules reserve stable public import locations for later L3 implementation.
"""

MODEL_ID = "cross_source_reconciliation_model"
REAL_EXECUTION_ALLOWED = False

def describe():
    return {"model_id": MODEL_ID, "status": "scaffold_ready", "real_execution_allowed": False}
