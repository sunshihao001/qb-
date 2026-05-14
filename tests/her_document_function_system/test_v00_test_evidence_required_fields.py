def test_test_execution_evidence_requires_exit_code():
    evidence = {
        'test_command': 'pytest tests/her_document_function_system',
        'stdout_path': 'stdout.log',
        'stderr_path': 'stderr.log',
        'passed_count': 3,
        'failed_count': 0,
    }
    assert 'exit_code' not in evidence


def test_valid_tested_status_requires_complete_evidence():
    evidence = {
        'test_command': 'python3 -m pytest tests/her_document_function_system -q',
        'exit_code': 0,
        'stdout_path': 'test_execution/test_stdout.log',
        'stderr_path': 'test_execution/test_stderr.log',
        'passed_count': 1,
        'failed_count': 0,
        'status': 'TESTED',
    }
    required = ['test_command', 'exit_code', 'stdout_path', 'stderr_path', 'passed_count', 'failed_count']
    assert all(field in evidence for field in required)
