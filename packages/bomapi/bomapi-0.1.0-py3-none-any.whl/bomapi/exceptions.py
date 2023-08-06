import httpx


class BomAPIError(Exception):
    """
    Common API exception
    """


class ResultError(BomAPIError):
    """
    Error when an unexpected result is returned
    """

    def __init__(self, message: str, response: httpx.Response):
        self.message = message
        self.response = response


class ResultNotFound(BomAPIError):
    """
    Item was not found result
    """
