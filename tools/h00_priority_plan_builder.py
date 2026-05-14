def build_priority_plan(items):
    return [{"queue_item_id": i["queue_item_id"], "priority": i["priority"]} for i in items]
