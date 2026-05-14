from .data_quality_evaluator import evaluate_data_quality, STATUS_TO_HANDOFF
def score_data_quality(*a, **k):
    return evaluate_data_quality(*a, **k)
