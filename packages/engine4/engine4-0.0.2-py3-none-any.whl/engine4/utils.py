"""Utility functions"""


def create_authorization_header(token: str) -> str:
    """
    Creates the authorization header for the ENGINE4 API.
    :param token: API Token
    :return: Authorization Header
    """
    return f"Bearer {token}"
