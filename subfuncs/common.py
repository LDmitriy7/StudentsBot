def to_list(obj):
    if isinstance(obj, (list, tuple)):
        return obj
    return [obj]


def find_objects(query_text: str, objects: set[str], limit=20) -> set[str]:
    """Find string with query_text (case insensitive)"""
    results = set()

    for o in objects:
        if query_text.lower() in o.lower():
            results.add(o)
            if len(results) >= limit:
                break
    return results
