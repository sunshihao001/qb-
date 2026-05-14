import pytest


@pytest.mark.xfail(reason='Negative assertion fixture intentionally encodes forbidden state for regression checking', strict=True)
def test_h00_no_queue_completed_without_execution():
    queue_state = {'queue_status': 'QUEUE_READY_WITH_GAPS', 'task_status': 'ITEM_COMPLETED', 'downstream_executed': False}
    assert queue_state['task_status'] != 'ITEM_COMPLETED' or queue_state['downstream_executed'] is True
