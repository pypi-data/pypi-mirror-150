class ClientError(Exception):
    """Raised when:

    - type from user or from Clickhouse is unrecognized;

    - user tries to pass arguments to not insert queries;

    - Clickhouse returns some errors.
    """


class GetObjectException(Exception):
    index = -1

    def __init__(
        self,
        exception: Exception,
        index=-1,
    ):
        self.index = index
        super().__init__(exception)
