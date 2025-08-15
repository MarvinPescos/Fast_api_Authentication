from app.errors import BalanceHubException

class TokenError(BalanceHubException):
    """Base token exception"""
    pass

class InvalidTokenError(TokenError):
    """Token is invalid or malformed"""
    pass

class ExpiredTokenError(TokenError):
    """Token has expired"""
    pass

class RevokedTokenError(TokenError):
    """Token has been revoked"""
    pass

class MissingTokenError(TokenError):
    """Required token is missing"""
    pass

class SessionExpiredError(TokenError):
    """User session has expired"""
    pass

class SessionNotFoundError(TokenError):
    """User session not found"""
    pass
