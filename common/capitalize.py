def capitalize(string: str) -> str:
    return "".join([string[:1].upper(), string[1:]])


def decapitalize(string: str) -> str:
    return "".join([string[:1].lower(), string[1:]])
