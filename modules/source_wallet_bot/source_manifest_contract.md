# Source Manifest Contract

## Purpose
Every Source & Wallet Intelligence Bot interface call must write a source manifest record.

## Required fields
- source_name
- endpoint
- request_started_at
- response_received_at
- provider_timestamp
- raw_response_path
- status
- error_message
- field_mapping_version

## Status enum
- success
- partial
- failed
- skipped
- missing_package
- parse_error

## Time rules
- request_started_at <= response_received_at
- provider_timestamp must be null if provider did not return a timestamp
- provider_timestamp cannot be fabricated from retrieved_at without fallback marks

## Endpoint rule
Endpoints must be redacted for sensitive query strings, API keys, tokens, or private parameters.

## Error rule
error_message is null on success, text on failure/partial.
