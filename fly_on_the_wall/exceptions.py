class UserCreationError(Exception):
    """ Raised when a User cannot be created """


class UserLoadError(Exception):
    """ Raised when a User cannot be loaded """


class MissingParametersError(Exception):
    """Raised when a Lambda doesn't receive all
    required paramters in its event"""
