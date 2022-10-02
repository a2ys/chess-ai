class ChessErrors(Exception):
    """Base class for exceptions in this module."""
    pass


class InvalidFenError(ChessErrors):
    """Exception raised for invalid FEN strings.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


class InvalidColorError(ChessErrors):
    """Exception raised for invalid color string.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


class NoKingError(ChessErrors):
    """Exception raised for no king in the FEN string.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


class KingCapturedError(ChessErrors):
    """Exception raised when king captured.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str) -> None:
        self.message = message


class InvalidMoveIdentifier(ChessErrors):
    """Exception raised when an invalid move identifier is given to the const.spl_move_identifier method.

        Attributes:
            message -- explanation of the error
        """

    def __init__(self, message: str) -> None:
        self.message = message
