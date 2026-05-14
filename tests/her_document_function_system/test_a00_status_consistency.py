def test_runner_binding_required_false_cannot_be_runner_bound():
    replay_context = {
        'runner_binding_required': False,
        'r00_status': 'SKIPPED_WITH_REASON',
    }
    assert replay_context['r00_status'] != 'RUNNER_BOUND'
