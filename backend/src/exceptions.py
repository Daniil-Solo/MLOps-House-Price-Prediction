"""Main exception base classes."""


class ApplicationException(Exception):
    """Base application error."""

    def __init__(self, message: str, status: int) -> None:
        """Set values.

        :param message:
        :param status:
        """
        self.message = message
        self.status = status


class GeocodingError(ApplicationException):
    """Error with geocoding address."""

    pass


class DistrictFindError(ApplicationException):
    """Error with finding district for point."""

    pass
