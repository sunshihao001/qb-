import json
from pathlib import Path


def test_controller_registry_json_is_parseable_and_has_controllers():
    path = Path('/root/sikk-gmgn/system/her_document_function_system/registry/controller_registry.json')
    data = json.loads(path.read_text())
    controllers = data.get('registered_controllers', [])
    assert controllers
    assert any(c.get('controller_id') == 'V00' for c in controllers)
