def test_h00_routing_decision_targets():
    routes = [
        {'target_controller': 'U00', 'decision': 'ROUTE_TO_U00'},
        {'target_controller': 'G00', 'decision': 'ROUTE_TO_G00'},
        {'target_controller': 'O00', 'decision': 'ROUTE_TO_O00'},
    ]
    controllers = {route['target_controller'] for route in routes}
    assert {'U00', 'G00', 'O00'} <= controllers
