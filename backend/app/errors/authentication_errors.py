from app.errors import BalanceHubException

class AuthenticationError(BalanceHubException):
    """Base authentication exception"""
    pass

class InvalidCredentialsError(AuthenticationError):
    """Invalid username or password"""
    pass

class AccountNotFoundError(AuthenticationError):
    """User account does not exist"""
    pass

class AccountDisabledError(AuthenticationError):
    """User account is disabled"""
    pass

class AccountLockedError(AuthenticationError):
    """User account is temporarily locked"""
    pass

class AccountSuspendedError(AuthenticationError):
    """User account is suspended"""
    pass

class PasswordExpiredError(AuthenticationError):
    """User password has expired"""
    pass

class TooManyLoginAttemptsError(AuthenticationError):
    """Too many failed login attempts"""
    pass

class EmailNotVerifiedError(AuthenticationError):
    """Email address not verified"""
    pass

class PasswordHashingError(AuthenticationError):
    """Failed to hash password"""
    pass