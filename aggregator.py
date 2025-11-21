def compile_report(data, aggregations=None, groupings=None):
    """
    data: dict[str, Any]
        Arbitrary datasets, e.g. {"orders": [...], "customers": [...]}

    aggregations: dict[str, callable]
        Each function receives the full `data` dict and returns a value.

    groupings: dict[str, dict]
        Each grouping entry defines:
            - "source": the name of a list in `data`
            - "keys": iterable of group keys
            - "fn": function(item, key) -> bool, decides if item belongs in group
    """
    result = {}

    # Run aggregations
    if aggregations:
        for name, fn in aggregations.items():
            result[name] = fn(data)

    # Run groupings
    if groupings:
        grouped_result = {}
        for group_name, cfg in groupings.items():
            source = cfg["source"]
            keys = cfg["keys"]
            fn = cfg["fn"]

            grouped_result[group_name] = {
                key: [item for item in data[source] if fn(item, key)]
                for key in keys
            }

        result["groups"] = grouped_result

    return result

