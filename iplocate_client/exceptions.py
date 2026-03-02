class IPLocateError(Exception):
    pass


class RateLimitError(IPLocateError):
    pass


class InvalidIPError(IPLocateError):
    pass