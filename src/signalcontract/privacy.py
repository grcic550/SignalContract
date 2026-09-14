PRIVATE_FIELDS = {
    "password",
    "passwd",
    "api_key",
    "access_token",
    "refresh_token",
    "secret",
}


def contains_private_fields(data: object) -> bool:
    """Return True if data contains any forbidden
    private field names."""

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(key, str) and key.lower() in PRIVATE_FIELDS:
                return True

            if contains_private_fields(value):
                return True

    elif isinstance(data, list):
        return any(contains_private_fields(item) for item in data)

    return False
