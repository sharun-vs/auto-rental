from secrets import token_urlsafe


def new_uid():
    return token_urlsafe(8)
