from app.errors import BalanceHubException

class AuthorizationError(BalanceHubException):
    """Base authorization exception"""
    pass

class PermissionDeniedError(AuthorizationError):
    """User lacks required permissions"""
    pass

class RoleNotAssignedError(AuthorizationError):
    """Required role not assigned to user"""
    pass

class ResourceAccessDeniedError(AuthorizationError):
    """Access denied to specific resource"""
    pass

class InsufficientPrivilegesError(AuthorizationError):
    """User has insufficient privileges"""
    pass


# =============================================================================
# TOKEN/SESSION ERRORS
# =============================================================================

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
