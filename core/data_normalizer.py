def simplify_items(items):
    cleaned = []

    for item in items:
        entry = {"name": item["name"]}

        for col in item["column_values"]:
            entry[col["id"]] = col["text"]

        cleaned.append(entry)

    return cleaned