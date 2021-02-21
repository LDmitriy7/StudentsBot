def find_strings(query_text: str, objects: set[str], limit=20) -> set[str]:
    """Find strings with query_text (case insensitive)"""
    results = set()

    for o in objects:
        if query_text.lower() in o.lower():
            results.add(o)
            if len(results) >= limit:
                break
    return results


def count_avg_values(objects_list: list[dict], obj_fields: list) -> dict:
    """Count average value for each dict's field in list of dicts."""
    avg_values = {field: 0 for field in obj_fields}

    for object_dict in objects_list:
        for field, amount in object_dict.items():
            avg_values[field] += amount

    objects_amount = len(objects_list) or 1
    for field, amount in avg_values.items():
        avg_values[field] /= objects_amount

    return avg_values



