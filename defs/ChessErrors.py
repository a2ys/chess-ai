class ChessErrors(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidFenError(ChessErrors):
    """Exception raised for invalid FEN strings.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class InvalidColorError(ChessErrors):
    """Exception raised for invalid color strings.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class NoKingError(ChessErrors):
    """Exception raised for no king on the board.py.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class KingCapturedError(ChessErrors):
    """Exception raised when king captured.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
