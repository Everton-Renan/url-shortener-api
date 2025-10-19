import secrets


def generate_url(nbytes: int | None):
    return secrets.token_urlsafe(nbytes)
