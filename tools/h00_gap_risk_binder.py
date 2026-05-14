def bind_gap_risk(items):
    return [{"queue_item_id": i["queue_item_id"], "gap_refs": i.get("gap_refs", [])} for i in items]
