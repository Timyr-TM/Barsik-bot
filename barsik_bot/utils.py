def list_format(items: list[str]):
    data = ""
    for item in items:
        data += f"- {item}\n"
    return data
