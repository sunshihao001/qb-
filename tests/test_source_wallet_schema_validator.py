import pytest

from modules.source_wallet_bot.errors import ForbiddenFieldError, SchemaValidationError
from modules.source_wallet_bot.schema_validator import (
    assert_no_forbidden_fields,
    validate_required_keys,
    validate_source_wallet_design_package,
)


def test_validate_required_keys_passes_for_complete_payload():
    validate_required_keys({'a': 1, 'b': 2}, ['a', 'b'])


def test_validate_required_keys_reports_missing_key():
    with pytest.raises(SchemaValidationError) as exc:
        validate_required_keys({'a': 1}, ['a', 'b'])
    assert 'b' in str(exc.value)


def test_forbidden_handoff_fields_are_rejected():
    with pytest.raises(ForbiddenFieldError):
        assert_no_forbidden_fields({'token_address': 'TOKEN', 'PAPER_READY': True})


def test_design_package_validator_finds_required_files():
    result = validate_source_wallet_design_package('/root/sikk-gmgn')
    assert result['ok'] is True
    assert not result['missing_files']
