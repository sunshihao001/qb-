def test_rule_logic_rejects_ai_judgment_without_fields():
    rule = {
        'rule_id': 'rule_bad_ai_only',
        'calculation_method': 'AI 判断',
        'output_status': 'PASSED',
    }
    assert 'input_fields' not in rule


def test_rule_logic_requires_output_status():
    rule = {
        'rule_id': 'rule_missing_output',
        'rule_type': 'status_integrity',
        'input_fields': ['test_execution_evidence'],
        'calculation_method': 'deterministic',
        'threshold_or_condition': 'exit_code == 0',
        'positive_evidence': ['exit_code'],
        'counter_evidence': [],
        'failure_condition': 'exit_code != 0',
        'trace_required': True,
    }
    assert 'output_status' not in rule
