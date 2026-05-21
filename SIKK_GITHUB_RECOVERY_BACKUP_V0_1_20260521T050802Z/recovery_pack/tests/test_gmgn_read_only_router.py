from adapters.gmgn_read_only_router import GMGNReadOnlyRouter


def test_gmgn_router_routes_backbone_to_canonical_consumers():
    router = GMGNReadOnlyRouter()
    routes = router.list_routes()
    assert len(routes) >= 7
    route_ids = {r['route_id'] for r in routes}
    assert {'token_info','market_pool','top_holders','trader_profit','security_read_if_safe'}.issubset(route_ids)
    for route in routes:
        assert route['read_only'] is True
        assert route['paper_only_boundary'] is True
        assert route['backbone_step'] == 1
        assert route['s_stage'] == 'S01'
        assert route['r_stage'] == ['R02','R03']
        assert 'SourceToCanonicalMapping' in route['downstream_consumer']
        assert route['mapping_owner'] == 'GMGN_SOURCE_TO_SIKK_CANONICAL_MAPPING_RUN'
        assert not any(bad in route['operation'] for bad in ['swap','sign','broadcast','quote'])


def test_gmgn_router_blocks_forbidden_operations():
    router = GMGNReadOnlyRouter()
    for op in ['swap','gmgn-swap','gmgn-cooking','route_quote','order_quote','sign_transaction','broadcast_transaction','live_trading']:
        try:
            router.assert_operation_allowed(op)
        except ValueError as exc:
            assert 'gmgn_operation_not_allowed' in str(exc)
        else:
            raise AssertionError(f'{op} should be blocked')


def test_gmgn_router_request_plan_is_stage_metadata_safe():
    plan = GMGNReadOnlyRouter().build_request_plan('TOKEN', 'solana')
    assert plan['mode'] == 'READ_ONLY_ROUTE_PLAN'
    assert plan['next_backbone_consumer'] == 'GMGN_SOURCE_TO_SIKK_CANONICAL_MAPPING_RUN'
    assert plan['stage_metadata']['sr_physical_split_allowed'] is False
    safety = plan['safety_boundary']
    assert safety['read_only'] is True
    assert safety['swap_allowed'] is False
    assert safety['route_quote_allowed'] is False
    assert safety['order_quote_allowed'] is False
    assert safety['private_key_required'] is False
    assert safety['signing_allowed'] is False
    assert safety['broadcast_allowed'] is False
    assert safety['live_trading_allowed'] is False
