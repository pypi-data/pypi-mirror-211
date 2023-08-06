from vecdb import types


def process_token(token: str) -> types.Credentials:
    splitted = token.split(":")
    if len(splitted) > 3:
        splitted = splitted[:3]
    return types.Credentials(*splitted)
