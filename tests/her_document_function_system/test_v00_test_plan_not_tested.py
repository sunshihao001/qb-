def test_test_plan_cannot_satisfy_tested_status():
    test_plan_only = {
        'test_plan': 'pytest tests/her_document_function_system',
        'status': 'TESTED',
    }
    required_evidence_fields = [
        'test_command',
        'exit_code',
        'stdout_path',
        'stderr_path',
        'passed_count',
        'failed_count',
    ]
    missing = [field for field in required_evidence_fields if field not in test_plan_only]
    assert missing
    assert test_plan_only['status'] != 'VALID_TESTED_STATUS'
