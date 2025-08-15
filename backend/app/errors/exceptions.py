class BalanceHubException(Exception):
    """Base exception for all BalanceHub errors"""
    def __init__(self, message: str, error_code: str = None, context: dict = None) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.__context__ = context or {}