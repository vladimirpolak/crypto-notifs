# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class CommentValidationError(Error):
    """Raised when instagram request isn't valid."""
    pass
